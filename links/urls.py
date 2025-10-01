from django.urls import path

from .views import (
    MyPageView,DashboardView,LinkListView,LinkDetailView,LinkCreateView,LinkUpdateView,
    LinkDeleteView
)

app_name = "links"

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('my_page/<slug:slug>/', MyPageView.as_view(), name='my-page'),
    path('link/list/', LinkListView.as_view(), name='link-list'),
    path('link/detail/<int:pk>/', LinkDetailView.as_view(), name='link-detail'),
    path('link/create/', LinkCreateView.as_view(), name='link-create'),
    path('link/update/<int:pk>/', LinkUpdateView.as_view(), name="link-update"),
    path('link/delete/<int:pk>/', LinkDeleteView.as_view(), name='link-delete')
]