from django.db import models

# Create your models here.
from accounts.models import UserProfile
from accounts.utils import CreatedUpdateAt


class Notification(CreatedUpdateAt):
    GAME = "GA"
    FRIEND_REQUEST = 'FR'

    TYPE = (
        (GAME, "Game"),
        (FRIEND_REQUEST, "Friend_request")
    )
    notification_type = models.CharField(max_length=2, choices=TYPE, default=None)
    sender = models.ForeignKey(UserProfile, related_name='sender', on_delete=models.CASCADE, default='')
    receiver = models.ForeignKey(UserProfile, related_name='receiver', on_delete=models.CASCADE, default='')
    active = models.BooleanField(default=True)
