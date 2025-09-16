import pytest
from django.contrib.auth import get_user_model

from accounts.forms import (
    RegisterForm,LoginForm,PasswordResetRequestForm,PasswordResetConfirmForm,ProfileForm
)

User=get_user_model()

@pytest.fixture
def user(db):
    return User.objects.create_user(
        username='test',email='test@gmail.com',password='123456789'
    )

@pytest.mark.django_db
def test_register_form():
    data = {
        'username':'ali','email':'ali@gmail.com','password':'Test12345',
        'confirm_password':'Test12345'
    }
    form = RegisterForm(data=data)
    assert form.is_valid() == True

@pytest.mark.django_db
def test_login_form(user):
    data = {
        'username':user.username,
        'password':'123456789'
    }
    form = LoginForm(data=data)
    assert form.is_valid() == True

@pytest.mark.django_db
def test_password_reset_request_form(user):
    data = {
        'email':user.email
    }
    form = PasswordResetRequestForm(data=data)
    assert form.is_valid() == True

@pytest.mark.django_db
def test_password_reset_confirm_form(user):
    data = {
        'password':'9191919187',
        'confirm_password':'9191919187'
    }
    form = PasswordResetConfirmForm(data=data, context={'user':user})
    assert form.is_valid() == True

@pytest.mark.django_db
def test_profile_form(user):
    data = {
        'email':'max@gmail.com'
    }
    form = ProfileForm(data=data, instance=user)
    assert form.is_valid() == True