import json
import smtplib

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.utils.decorators import method_decorator
from django.views import View
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.generic import FormView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import authenticate, logout, login
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework.response import Response

from .forms import RegisterForm
from .permissions import friends_permissions
from .serializers import *
from .tasks import send_email
from rest_framework.authtoken.models import Token


# # For API
# class UserRegister(APIView):
#     """
#     Creating a new user with a get method for some time.
#     """
#
#     def get(self):
#         users = UserProfile.objects.all()
#         serializer = CreateUserProfileSerializer(users, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = CreateUserProfileSerializer(data=request.data)
#         if serializer.is_valid():
#             subject = 'Welcoming message!'
#             message = 'Welcome to our company!'
#             to_email = serializer.validated_data['email']
#             send_email(subject, message, to_email)
#             serializer.save()
#             token, created = Token.objects.get_or_create(user=serializer.instance)
#             return Response(token.key)
#         else:
#             return Response(serializer.errors)
#
#
# class UserLogin(APIView):
#     """
#     Authenticate user
#     :return token
#     """
#
#     def post(self, request):
#         serializer = AuthTokenSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.validated_data['user']
#             token, created = Token.objects.get_or_create(user=user)
#             return Response({'token': token.key})
#         else:
#             return Response(serializer.errors)
#
#
# class UserLogout(APIView):
#     """
#     Destroying user's auth login
#     """
#
#     def post(self, request):
#         return request.user.token.delete()
#

# For templates
@require_http_methods(["POST"])
def add_friend(request, *args, **kwargs):
    user_profile = kwargs['username']
    user_visitior = get_object_or_404(UserProfile, username=user_profile)
    logged_user = get_object_or_404(UserProfile, username=request.user.username)
    logged_user.friends.add(user_visitior)
    return HttpResponseRedirect(request.path_info)


def post_like(request, *args, **kwargs):
    post = Post.objects.get(uuid=kwargs['uuid'])
    post.increment_post_likes
    post.save(update_fields=["likes"])
    return HttpResponseRedirect('/home')


def comment_like(request, *args, **kwargs):
    comment = Comment.objects.get(uuid=kwargs['uuid'])
    comment.increment_comment_likes
    comment.save(update_fields=["likes"])
    return HttpResponseRedirect('/home')


def reply_like(request, *args, **kwargs):
    reply = CommentReply.objects.get(uuid=kwargs['uuid'])
    reply.increment_reply_likes
    reply.save(update_fields=["likes"])
    return HttpResponseRedirect('/home')


def post_comment(request, *args, **kwargs):
    post = Post.objects.get(uuid=kwargs['uuid'])
    Comment.objects.create(
        post=post,
        commenter=request.user,
        text=request.POST.get('comment')
    )
    return HttpResponseRedirect('/home')


def comment_reply(request, *args, **kwargs):
    comment = Comment.objects.get(uuid=kwargs['uuid'])
    CommentReply.objects.create(
        comment=comment,
        replier=request.user,
        text=request.POST.get('reply')
    )
    return HttpResponseRedirect('/home')


def delete_post(request, *args, **kwargs):
    post_uuid = kwargs['uuid']
    post = Post.objects.get(uuid=post_uuid)
    post.delete()
    return HttpResponseRedirect('/home')


def register(request):
    template_name = 'register.html'
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return HttpResponseRedirect('/home')
    else:
        form = RegisterForm()
    return render(request, template_name, {'form': form})


def logoutView(request):
    if request.method == 'GET':
        logout(request)
        return HttpResponseRedirect(settings.LOGOUT_REDIRECT_URL)


class Login(LoginView):
    template_name = 'login.html'


class ChangePassword(PasswordChangeView):
    success_url = '/login'
    template_name = 'change_password.html'


class Home(View):
    template_name = 'home.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        friends = [friend for friend in
                   UserProfile.objects.filter(username=self.request.user).values_list('friends', flat=True)]
        friends.append(self.request.user.id)
        posts = Post.objects.filter(user__in=friends).order_by('-created_date')
        comments = Comment.objects.all()
        comment_replies = CommentReply.objects.all()
        context = {'posts': posts, 'comments': comments, 'comment_replies': comment_replies}
        return render(request, self.template_name, context)

    def post(self, request):
        text = self.request.POST.get('text')
        post_image = self.request.FILES.get('post_image')
        if text:
            new_post = Post.objects.create(user=self.request.user, text=text, post_image=post_image)
            new_post.save()
        return HttpResponseRedirect(self.request.path_info)


class FriendProfile(View):
    template_name = 'friend_profile.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if friends_permissions(request, *args, **kwargs):
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404('You have permission to view profiles of ONLY your friends.')

    def get(self, request, *args, **kwargs):
        username = self.kwargs.get('username')
        user = UserProfile.objects.get(username=username)
        posts = Post.objects.filter(user=user.id).order_by('-created_date')
        context = {'posts': posts, 'user_profile': user}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        text = self.request.POST.get('text')
        post_image = self.request.FILES.get('post_image')
        if text:
            new_post = Post.objects.create(user=self.request.user, text=text, post_image=post_image)
            new_post.save()
        return HttpResponseRedirect(self.request.path_info)
