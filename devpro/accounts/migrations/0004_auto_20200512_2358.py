# Generated by Django 3.0.5 on 2020-05-12 23:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_post_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='created_at'),
        ),
        migrations.AddField(
            model_name='comment',
            name='edited_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='edited_at'),
        ),
        migrations.AddField(
            model_name='post',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='created_at'),
        ),
        migrations.AddField(
            model_name='post',
            name='edited_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='edited_at'),
        ),
    ]
