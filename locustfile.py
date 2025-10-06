from random import randint as rnd
from locust import HttpUser, task, between
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

class WebsiteUser(HttpUser):
    host = settings.SITE_DOMAIN
    wait_time = between(1,5)

    def on_start(self):
        self.user = User.objects.create_user(
            username='test', 
            email='test@gmail.com', 
            password='123456789'
        )
        

    @task
    def register(self):
        rand = rnd(1,1000000)
        self.client.post("/register/", data={
            'username': f'ali{rand}',
            'email': f'ali{rand}@gmail.com',
            'avatar': '',
            'password': '123456789',
            'confirm_password': '123456789'
        })
    
    @task
    def login(self):
        self.client.post("/login/", data={
            'username': self.user.username,
            'password': '123456789'
        })
    
    @task
    def my_page(self):
        self.client.get(f"/my_page/{self.user.slug}/")