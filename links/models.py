from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Link(models.Model):
    class LinkStatus(models.TextChoices):
        enable = 'Enable'
        disable = 'Disable'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='link', verbose_name='link')
    title = models.CharField(max_length=150,verbose_name='title')
    url = models.URLField(verbose_name='url')
    icon = models.ImageField(upload_to='links/icons', verbose_name='icon')
    status = models.BooleanField(choices=LinkStatus, default=LinkStatus.enable, verbose_name='status')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created date')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Link'
        verbose_name_plural = 'Links'
