import pytest
from django.contrib.auth import get_user_model

from links.models import (
    Link,PageView
)

User = get_user_model()

@pytest.fixture
def user(db):
    return User.objects.create_user(
        username='test', email='test@gmail.com', password='123456789'
    )

@pytest.mark.django_db
def test_link_model(user):
    link = Link.objects.create(
        user=user, 
        title='github',
        url='https://github.com/Esmat434/',
    )
    assert link.user.username == 'test'
    assert link.title == 'github'
    assert link.url == 'https://github.com/Esmat434/'

@pytest.mark.django_db
def test_page_view_model(user):
    view = PageView.objects.create(
        user=user, 
        path='https://github.com/Esmat434/',
        ip_address='127.0.0.1',
        user_agent='Mobile'
    )
    assert view.user.username == 'test'
    assert view.path == 'https://github.com/Esmat434/'
    assert view.ip_address == '127.0.0.1'
    assert view.user_agent == 'Mobile'