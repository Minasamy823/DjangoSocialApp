from __future__ import absolute_import, unicode_literals
import smtplib
from datetime import timedelta
from celery.schedules import crontab
from celery.task import periodic_task
from django.core.mail import send_mail, EmailMessage
from celery import shared_task

# @periodic_task(run_every=(timedelta(seconds=3)), name='my first_task')
# def printy():
#     print('test celery redis')


@shared_task
def send_email(subject, message, to_email):
    try:
        email = EmailMessage(subject,
                             message,
                             to=[to_email],
                             )
        email.send()
    except smtplib.SMTPException as ex:
        raise ValueError('Sending failed')
