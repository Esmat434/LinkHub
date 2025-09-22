from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Link(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='link', verbose_name='link')
    title = models.CharField(max_length=150, unique=True,verbose_name='title')
    url = models.URLField(verbose_name='url')
    icon = models.ImageField(upload_to='links/icons')
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Link'
        verbose_name_plural = 'Links'
