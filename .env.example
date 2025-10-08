# Django Settings
DEBUG=False
SECRET_KEY=your_secret_key_here 

ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:8080,http://127.0.0.1:8080

# ===================================================================
# Database INITIALIZATION variables FOR MYSQL CONTAINER (این بخش برای خود کانتینر MySQL است)
# ===================================================================
MYSQL_DATABASE=your_db_name
MYSQL_USER=your_db_user
MYSQL_PASSWORD=your_db_password
MYSQL_ROOT_PASSWORD=your_db_root_password

# Celery for redis
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# Email Settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your_password_or_app_password #<-- نکته مهم بعدی

# SITE_DOMAIN
SITE_DOMAIN=http://localhost:8080