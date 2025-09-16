from celery import shared_task
from .email import send_verification_email_async

@shared_task
def send_verification_email(to,subject,username,link):
    send_verification_email_async(to,subject,username,link) 