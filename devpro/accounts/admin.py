from django.contrib import admin
from .models import *

# from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter

admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(CommentReply)

# @admin.register(UserProfile)
# class UserAdmin(admin.ModelAdmin):
# list_filter = [('created_at', DateRangeFilter), 'is_staff']
