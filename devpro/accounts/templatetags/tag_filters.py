from django import template

from ..models import *

register = template.Library()


@register.filter
def qs_filter(value, filter_by):
    return Comment.objects.filter(post=filter_by)


@register.filter
def comment_replies_filter(value, comment):
    print(CommentReply.objects.filter(comment=comment))
    return CommentReply.objects.filter(comment=comment)
