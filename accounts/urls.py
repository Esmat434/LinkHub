from django.urls import path
from .views import (
    RegisterView,LoginView,LogoutView,PasswordResetRequestView,PasswordResetConfirmView,
    ProfileView,ProfileUpdateView
)

app_name='accounts'

urlpatterns=[
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_reset_request/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password_reset_confirm/<uuid:uuid>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile-update')
]