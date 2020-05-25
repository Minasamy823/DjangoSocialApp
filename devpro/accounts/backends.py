from django.contrib.auth.backends import BaseBackend

from .models import UserProfile


class PhoneNumberBackend(BaseBackend):
    """
    Authenticates against phone numbers.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return
        try:
            user = UserProfile.objects.get(phone_number=username)
            if user.check_password(password):
                return user
        except UserProfile.DoesNotExist:
            return None  # return None if custom user model does not exist

    def get_user(self, user_id):
        try:
            return UserProfile.objects.get(pk=user_id)
        except UserProfile.DoesNotExist:
            return None

