from uuid import uuid4
from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.utils import timezone


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    slug = models.SlugField(unique=True)
    avatar = models.ImageField(upload_to='users/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        return super().save(*args,**kwargs)

class ForgotPassword(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='forgot_password')
    token = models.UUIDField(default=uuid4)
    created_at = models.DateField(auto_now_add=True)

    def check_token_expiration_time(self):
        expire_time = self.created_at + timedelta(days=1)
        if timezone.now() > expire_time:
            raise ValueError("Your token is expired.")
        return True
