# Generated by Django 3.0.5 on 2020-05-13 22:15

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20200513_2110'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AddField(
            model_name='commentreply',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
