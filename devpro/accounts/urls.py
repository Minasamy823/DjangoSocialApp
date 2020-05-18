from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path
from .views import *

urlpatterns = [
    path('register', register),
    path('login/', Login.as_view()),
    path('logout/', logoutView, name='logout'),
    path('changepassword/', ChangePassword.as_view(), name='change_password'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('home/', Home.as_view(), name='home'),
    path('post/like/<uuid:uuid>', post_like, name='post_like'),
    path('comment/like/<uuid:uuid>', comment_like, name='comment_like'),
    path('reply/like/<uuid:uuid>', reply_like, name='reply_like'),
    path('post/comment/<uuid:uuid>', post_comment, name='post_comment'),
    path('comment/reply/<uuid:uuid>', comment_reply, name='comment_reply'),
    path('<uuid:uuid>/', delete_post, name='delete_post'),
    path('<str:username>/', login_required(FriendProfile.as_view()), name='friend_profile'),
]
