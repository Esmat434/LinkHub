import pytest
from django.contrib.auth import get_user_model

from accounts.models import (
    ForgotPassword
)

User=get_user_model()

@pytest.fixture
def user(db):
    return User.objects.create_user(
        username='test',email='test@gmail.com',password='123456789'        
    )

@pytest.mark.django_db
def test_custom_user_model():
    user = User.objects.create_user(
        username='ali',email='ali@gmail.com',password='Test12345'
    )
    assert user.username == 'ali'
    assert user.email == 'ali@gmail.com'

@pytest.mark.django_db
def test_forgot_password_model(user):
    token_instance = ForgotPassword.objects.create(
        user=user
    )
    assert token_instance.user == user