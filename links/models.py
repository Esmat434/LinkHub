from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Link(models.Model):
    class LinkStatus(models.TextChoices):
        enable = 'Enable'
        disable = 'Disable'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='links', verbose_name='link')
    title = models.CharField(max_length=150,verbose_name='title')
    url = models.URLField(verbose_name='url')
    icon = models.ImageField(upload_to='links/icons', verbose_name='icon', blank=True, null=True)
    status = models.CharField(max_length=10,choices=LinkStatus, default=LinkStatus.enable, verbose_name='status')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created date')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Link'
        verbose_name_plural = 'Links'

class PageView(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='pageview', verbose_name='User')
    path = models.CharField(max_length=255, verbose_name='Path')
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP_Address')
    user_agent = models.TextField(null=True, blank=True, verbose_name='User Agent')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created Date')

    def __str__(self):
        return f"IP: {self.ip_address} Related to: {self.user.username if self.user else 'Anonymous'}"
    
    class Meta:
        verbose_name = 'Page View'
        verbose_name_plural = 'Page Views'
