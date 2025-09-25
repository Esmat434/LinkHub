from django.contrib import admin

from .models import (
    Link,PageView
)

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ['user','title','url','status','created_at']

@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ['user','path','ip_address','user_agent','created_at']