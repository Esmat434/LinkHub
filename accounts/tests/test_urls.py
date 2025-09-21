import uuid
from django.urls import reverse

def test_register_url():
    url=reverse('accounts:register')
    assert url == '/register/'

def test_login_url():
    url=reverse('accounts:login')
    assert url == '/login/'

def test_logout_url():
    url=reverse('accounts:logout')
    assert url == '/logout/'

def test_password_reset_request_url():
    url=reverse('accounts:password-reset-request')
    assert url == '/password_reset_request/'

def test_password_reset_confirm_url():
    token = uuid.uuid4()
    url=reverse('accounts:password-reset-confirm', args=[token])
    assert url == f'/password_reset_confirm/{token}/'

def test_profile_url():
    url=reverse('accounts:profile')
    assert url == '/profile/'

def test_profile_update_url():
    url=reverse('accounts:profile-update')
    assert url == '/profile/update/'