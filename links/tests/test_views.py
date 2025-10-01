import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

from links.models import (
    Link
)

User = get_user_model()

@pytest.fixture
def user(db):
    return User.objects.create_user(
        username='test', email='test@gmail.com', password='123456789'
    )

@pytest.fixture
def auth_client(user,client):
    client.force_login(user=user)
    return client

@pytest.fixture
def link(user):
    return Link.objects.create(
        user=user, title='github', url='https://github.com/Esmat434/'
    )

class TestMyPageView:
    @pytest.fixture(autouse=True)
    def setUp(self,user,client):
        self.user=user
        self.client=client
    
    def test_get_method(self):
        url = reverse('links:my-page', args=[self.user.slug])
        response = self.client.get(url)

        assert response.status_code == 200

class TestDashboardView:
    @pytest.fixture(autouse=True)
    def setUp(self,user,auth_client):
        self.user=user
        self.client=auth_client
    
    def test_get_method(self):
        url = reverse('links:dashboard')
        response = self.client.get(url)

        assert response.status_code == 200

class TestLinkListView:
    @pytest.fixture(autouse=True)
    def setUp(self,auth_client):
        self.client = auth_client
    
    def test_get_method(self):
        url = reverse('links:link-list')
        response = self.client.get(url)

        assert response.status_code == 200

class TestLinkDetailView:
    @pytest.fixture(autouse=True)
    def setUp(self,auth_client,link):
        self.client = auth_client
        self.link = link
    
    def test_get_method(self):
        url = reverse('links:link-detail', args=[self.link.pk])
        response = self.client.get(url)

        assert response.status_code == 200

class TestLinkCreateView:
    @pytest.fixture(autouse=True)
    def setUp(self,auth_client):
        self.client = auth_client
        self.data = {
            'title':'github', 'url':'https://github.com/Esmat434/', 'icon':'', 
            'status':'Enable'
        }

    def test_get_method(self):
        url = reverse('links:link-create')
        response = self.client.get(url)

        assert response.status_code == 200
    
    def test_post_method(self):
        url = reverse('links:link-create')
        response = self.client.post(url, data=self.data)

        assert response.status_code == 302
    
class TestLinkUpdateView:
    @pytest.fixture(autouse=True)
    def setUp(self,auth_client,link):
        self.client = auth_client
        self.link = link
        self.data = {
            'title':'twitter', 'url':'https://twitter.com/Esmat434/', 'icon':'', 
            'status':'Enable'
        }
    
    def test_get_method(self):
        url = reverse('links:link-update', args=[self.link.pk])
        response = self.client.get(url)

        assert response.status_code == 200

    def test_post_method(self):
        url = reverse('links:link-update', args=[self.link.pk])
        response = self.client.post(url, data=self.data)

        assert response.status_code == 302

class TestLinkDeleteView:
    @pytest.fixture(autouse=True)
    def setUp(self,auth_client,link):
        self.client = auth_client
        self.link = link
    
    def test_get_method(self):
        url = reverse('links:link-delete', args=[self.link.pk])
        response = self.client.get(url)

        assert response.status_code == 302