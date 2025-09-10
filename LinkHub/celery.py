import os
from celery import Celery

# ست کردن تنظیمات جنگو برای celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LinkHub.settings')

app = Celery('LinkHub')

# خواندن تنظیمات celery از فایل settings.py جنگو
app.config_from_object('django.conf:settings', namespace='CELERY')

# شناسایی اتوماتیک همه‌ی task ها
app.autodiscover_tasks()