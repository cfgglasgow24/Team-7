# pages/urls.py

from django.urls import path
from pages import views

urlpatterns = [
    path("", views.home, name='home'),
    path("filter/", views.filter, name='filter'),
    path("request/", views.request, name='request'),
]