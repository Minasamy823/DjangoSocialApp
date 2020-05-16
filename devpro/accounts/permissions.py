from django.http import Http404
from django.shortcuts import get_object_or_404

from .models import UserProfile


def friends_permissions(request, *args, **kwargs):
    accessed_profile_username = kwargs.get('username')
    accessed_profile_user_id = get_object_or_404(UserProfile, username=accessed_profile_username).id
    friends = [friend for friend in
               UserProfile.objects.filter(username=request.user.username).values_list('friends', flat=True)]
    friends.append(accessed_profile_user_id)
    return accessed_profile_user_id in friends

