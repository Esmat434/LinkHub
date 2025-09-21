from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.conf import settings

from .models import (
    ForgotPassword
)
from .tasks import (
    send_verification_email
)

@receiver(post_save, sender=ForgotPassword)
def send_token_in_email_after_create_token(sender, instance, created, **kwargs):
    domain = getattr(settings, 'SITE_DOMAIN', 'http://localhost:8000')
    link = domain + reverse('accounts:password-reset-confirm', args=[instance.token])
    send_verification_email.delay(instance.user.email, 'Forgot Password Token', instance.user.username, link)
