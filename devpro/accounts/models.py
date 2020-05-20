from itertools import count
import uuid as uuid
from PIL import Image
from django.utils import timezone
from django.utils.datetime_safe import datetime
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from versatileimagefield.fields import VersatileImageField

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField

# from .utils import *
from .utils import LikeDislikeTextAbstract, CreatedUpdateAt


class PhoneNUmber(models.Model):
    phone_number = PhoneNumberField(unique=True, error_messages={'unique': 'already exists',
                                                                 'invalid': 'number must be Russian number starts '
                                                                            'with +7 or 8'})

    class Meta:
        abstract = True


class UserManager(BaseUserManager):

    def _create_user(self, email, username, password, **kwargs):
        """
        :param password:
        :param email:
        :param username:
        :param kwargs:
        :return: instance of a user without extra fields
        """
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create(self, email, username, password, **extra):
        """
        :param email:
        :param username:
        :param password:
        :param extra:
        :return: user instance with extra fields
        """
        extra.setdefault('is_staff', False)
        return self._create_user(email, username, password, **extra)

    def create_superuser(self, email, username, password=None, **extra):
        """
        :param email:
        :param username:
        :param password:
        :param extra:
        :return: super_user instance with extra fields
        """

        # if not extra['is_staff']:
        #     raise ValueError('Super user must be a stuff member')
        extra.setdefault('is_staff', True)
        extra.setdefault('is_superuser', True)
        return self._create_user(email, username, password, **extra)


class UserProfile(PhoneNUmber, AbstractBaseUser, PermissionsMixin):
    avatar = VersatileImageField(default='', blank=True)
    email = models.EmailField(max_length=200, blank=False, unique=True)
    username = models.CharField(max_length=200, blank=False, unique=True)
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    comment_user = models.CharField(max_length=200, blank=True, default='')
    friends = models.ManyToManyField("self", related_name='friends', blank=True)
    is_staff = models.BooleanField(help_text='Designates whether the user can log into this admin site.', default=False)
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    created_at = models.DateTimeField(help_text='date joined', default=timezone.now)

    class Meta:
        ordering = ['created_at']
        verbose_name = _('user')
        verbose_name_plural = _('users')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = UserManager()

    def __repr__(self):
        return f'Customized users models'

    def __str__(self):
        return self.username

    def get_full_name(self):
        """
        :return: return full name
        """
        return f'_{self.first_name} + _{self.last_name}'

    def get_short_name(self):
        """
        :return: first name
        """
        return f'_{self.first_name}'

    def save(self, *args, **kwargs):
        if not self.avatar:
            return super(UserProfile, self).save()
        super(UserProfile, self).save()
        image = Image.open(self.avatar)
        size = (70, 70)
        image = image.resize(size, Image.ANTIALIAS)
        image.save(self.avatar.path)


class Post(LikeDislikeTextAbstract, CreatedUpdateAt):
    ONLY_ME = "OM"
    PUBLIC = 'PU'
    EXCEPT_FRIENDS = 'EF'
    ONLY_FRIENDS = 'OF'

    VISIBILITY = (
        (ONLY_ME, "only_me"),
        (PUBLIC, "public"),
        (EXCEPT_FRIENDS, "except_friends"),
        (ONLY_FRIENDS, "only_friends")
    )
    visibility = models.CharField(max_length=2, choices=VISIBILITY, default=PUBLIC, blank=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(UserProfile, related_name='post', on_delete=models.CASCADE)
    post_image = VersatileImageField(default='', blank=True)

    class Meta:
        ordering = ('created_date',)

    @property
    def get_number_post_likes(self):
        return self.likes if self.likes > 0 else ''

    @property
    def increment_post_likes(self):
        self.likes += 1
        return self.likes

    @property
    def increment_post_dislikes(self):
        self.dislikes + 1
        return self.dislikes

    def save(self, *args, **kwargs):
        if not self.post_image:
            return super(Post, self).save()
        super(Post, self).save()
        image = Image.open(self.post_image)
        size = (600, 500)
        image = image.resize(size, Image.ANTIALIAS)
        image.save(self.post_image.path)


class Comment(LikeDislikeTextAbstract, CreatedUpdateAt):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    commenter = models.ForeignKey(UserProfile, related_name='commenter', on_delete=models.CASCADE)
    comment_image = VersatileImageField(default='', blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default='')

    class Meta:
        ordering = ('created_date',)

    @property
    def get_number_Comment_likes(self):
        return self.likes if self.likes > 0 else ''

    @property
    def get_comment_time_remains(self):
        date = (timezone.now() - self.created_date).days
        return f'Today' if date == 0 else f'{date} days'

    @property
    def increment_comment_likes(self):
        self.likes += 1
        return self.likes


class CommentReply(LikeDislikeTextAbstract, CreatedUpdateAt):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    replier = models.ForeignKey(UserProfile, related_name='replier', on_delete=models.CASCADE)
    reply_image = VersatileImageField(default='', blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_replies', default='')

    class Meta:
        ordering = ('created_date',)

    @property
    def increment_reply_likes(self):
        self.likes += 1
        return self.likes

    @property
    def get_number_reply_likes(self):
        return self.likes if self.likes > 0 else ''
