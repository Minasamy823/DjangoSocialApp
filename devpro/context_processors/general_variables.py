from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from notifications.models import Notification


def get_user_friend_requests(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(receiver=request.user, active=True)
        return {"notifications": notifications}
    else:
        return {"notifications": []}
