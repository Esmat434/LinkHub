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
    birth_date = models.DateField(blank=True, null=True)
    email_verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        return super().save(*args,**kwargs)

class Tokens(models.Model):
    class Token_Type(models.TextChoices):
        email_verified='email_verified','Email Verified'
        change_password='change_password','Change Password'
        forgot_password='forgot_password','Forgot Password'

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    type = models.CharField(max_length=100, choices=Token_Type, default=Token_Type.email_verified)
    token = models.UUIDField(default=uuid4)
    created_at = models.DateField(auto_now_add=True)

    def check_token_expiration_time(self):
        expire_time = self.created_at + timedelta(days=1)
        if timezone.now() > expire_time:
            raise ValueError("Your token is expired.")
        return True
