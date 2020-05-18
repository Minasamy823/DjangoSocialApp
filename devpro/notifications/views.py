from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from accounts.models import UserProfile
from .models import *


@require_http_methods(["POST"])
def send_friend_request(request, *args, **kwargs):
    notification_receiver_username = kwargs['username']
    notification_receiver = get_object_or_404(UserProfile, username=notification_receiver_username)
    notification_sender = get_object_or_404(UserProfile, username=request.user.username)
    Notification.objects.get_or_create(
        sender=notification_sender,
        receiver=notification_receiver,
        notification_type='FR',
        active=True,
    )
    return HttpResponseRedirect(f'/{notification_receiver_username}')


def confirm_friend_request(request, *args, **kwargs):
    notification = get_object_or_404(Notification,
                                     uuid=kwargs['uuid'],
                                     )
    logged_in_user = UserProfile.objects.get(username=request.user)
    logged_in_user.friends.add(notification.sender)
    notification.delete()
    return HttpResponseRedirect(f'/{logged_in_user.username}')


def reject_friend_request(request, *args, **kwargs):
    notification = get_object_or_404(Notification,
                                     uuid=kwargs['uuid'],
                                     )
    notification.delete()
    return HttpResponseRedirect(f'/{notification.receiver}')
