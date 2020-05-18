from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from .views import *

urlpatterns = [
    path('send_friend_request/<str:username>/', login_required(send_friend_request), name='send_friend_request'),
    path('confirm_friend_request/<uuid:uuid>/', login_required(confirm_friend_request), name='confirm_friend_request'),
    path('reject_friend_request/<uuid:uuid>/', login_required(reject_friend_request), name='reject_friend_request'),
]
urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
