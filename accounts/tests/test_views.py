import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

from accounts.models import (
    ForgotPassword
)

User=get_user_model()

@pytest.fixture
def user(db):
    password='123456789'
    user = User.objects.create_user(
        username='test',email='test@gmail.com',password=password
    )
    user.raw_password=password
    return user

@pytest.fixture
def auth_user(user,client):
    client.force_login(user)
    return client

class TestRegisterView:
    @pytest.fixture(autouse=True)
    def setUp(self,client):
        self.client=client
        self.data = {
            'username':'ali','email':'ali@gmail.com','password':'Test12345',
            'confirm_password':'Test12345'
        }
    
    def test_get_method_register_view(self):
        url = reverse('accounts:register')
        response = self.client.get(url)

        assert response.status_code == 200
    
    def test_post_method_register_view(self):
        url = reverse('accounts:register')
        response = self.client.post(url, data=self.data)

        assert response.status_code == 302

class TestLoginView:
    @pytest.fixture(autouse=True)
    def setUp(self,client,user):
        self.client=client
        self.data = {
            'username':user.username,
            'password':user.raw_password
        }
    
    def test_get_method_login_view(self):
        url = reverse('accounts:login')
        response = self.client.get(url)

        assert response.status_code == 200
    
    def test_post_method_login_view(self):
        url = reverse('accounts:login')
        response = self.client.post(url, data=self.data)
        
        assert response.status_code == 302

class TestLogoutView:
    @pytest.mark.django_db
    def setUp(self,auth_user):
        self.client = auth_user
    
    def test_get_method(self):
        url = reverse('accounts:logout')
        response = self.client.get(url)

        assert response.status_code == 200

class TestPasswordResetRequestView:
    @pytest.fixture(autouse=True)
    def setUp(self,client,user):
        self.client=client
        self.user=user
        self.data = {
            'email':'test@gmail.com'
        }
    
    def test_get_method_password_reset_request_view(self):
        url = reverse('accounts:password-reset-request')
        response = self.client.get(url)

        assert response.status_code == 200
    
    def test_post_method_password_reset_request_view(self):
        url = reverse('accounts:password-reset-request')
        response = self.client.post(url, data=self.data)

        assert response.status_code == 201

class TestPassowrdResetConfirmView:
    @pytest.fixture(autouse=True)
    def setUp(self,client,user):
        self.client=client
        self.token_instance = ForgotPassword.objects.create(user)
        self.data = {
            'password':'test919191',
            'confirm_password':'test919191'
        }
    
    def test_get_method_password_reset_confirm(self):
        url = reverse('accounts:password-reset-confirm', args=[self.token_instance])
        response = self.client.get(url)

        assert response.status_code == 200
    
    def test_post_method_validate(self):
        url = reverse('accounts:password-reset-confirm', args=[self.token_instance])
        response = self.client.post(url, data=self.data)

        assert response.status_code == 302

class TestProfileView:
    @pytest.fixture(autouse=True)
    def setUp(self,auth_user,user):
        self.client=auth_user
        self.user=user
    
    def test_get_method(self):
        url = reverse('accounts:profile')
        response = self.client.get(url)

        assert response.status_code == 200

class TestProfileUpdateView:
    @pytest.fixture(autouse=True)
    def setUp(self,auth_user):
        self.client=auth_user
        self.data = {
            'username':'alex'
        }
    
    def test_get_method(self):
        url = reverse('accounts:profile-update')
        response = self.client.get(url)

        assert response.status_code == 200
    
    def test_post_method(self):
        url = reverse('accounts:profile-update')
        response = self.client.get(url, data=self.data)

        assert response.status_code == 302