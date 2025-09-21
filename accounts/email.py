from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from celery import shared_task

@shared_task
def send_verification_email_async(to,subject,username,link):
    html_content=render_to_string('accounts/password_reset_email.html',{'username':username,'link':link})
    email=EmailMessage(subject,html_content,settings.EMAIL_HOST_USER,[to])
    email.content_subtype='html'

    try:
        email.send()
    except Exception as e:
        return e