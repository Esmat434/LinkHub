from django.urls import path

from .views import (
    MyPageView,DashboardView,LinkListView,LinkCreateView,LinkUpdateView
)

app_name = "links"

urlpatterns = [
    path('my_page/<slug:slug>/', MyPageView.as_view(), name='my_page'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('link/list/', LinkListView.as_view(), name='link_list'),
    path('link/create/', LinkCreateView.as_view(), name='link_create'),
    path('link/update/<int:pk>/', LinkUpdateView.as_view(), name="link_update")
]