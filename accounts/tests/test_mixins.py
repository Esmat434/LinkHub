import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

User=get_user_model()

@pytest.fixture
def user(db):
    password='123456789'
    user = User.objects.create_user(
        username='test',email='test@gmail.com',password=password
    )
    user.raw_password=password
    return user

@pytest.mark.django_db
def test_login_required_mixin(user,client):
    client.force_login(user)
    url = reverse('accounts:login')
    response = client.get(url)
    
    assert response.status_code == 200

@pytest.mark.django_db
def test_logout_required_mixin(client):
    url = reverse('accounts:register')
    response = client.get(url)

    assert response.status_code == 200