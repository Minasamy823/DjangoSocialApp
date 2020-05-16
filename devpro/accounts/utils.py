from django.db import models
from django.utils import timezone


class CreatedUpdateAt(models.Model):
    created_date = models.DateTimeField("created_at", default=timezone.now)
    edited_date = models.DateTimeField("edited_at", default=timezone.now)

    class Meta:
        abstract = True


class LikeDislikeTextAbstract(models.Model):
    text = models.TextField(max_length=1000, blank=False)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True
