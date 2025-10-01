import pytest
from django.contrib.auth import get_user_model

from links.models import (
    Link
)
from links.forms import (
    LinkCreationForm,LinkUpdateForm
)

User = get_user_model()

@pytest.fixture
def user(db):
    return User.objects.create_user(
        username='test', email='test@gmail.com', password='123456789'
    )

@pytest.fixture
def link(user):
    return Link.objects.create(
        user=user, title='github', url='https://github.com/Esmat434/'
    )

def test_link_creation_form(user):
    data = {
        'title':'github', 'url':'https://github.com/Esmat434/', 'icon':None, 'status':'Enable'
    }
    form = LinkCreationForm(data=data, user=user)
    assert form.is_valid() == True

def test_link_update_form(user,link):
    data = {
        'title':'my website', 'url':'http://esmatullah009.pythonanywhere.com', 'icon':None,
        'status':'Enable' 
    }
    form = LinkUpdateForm(data=data, instance=link, user=user)
    assert form.is_valid() == True