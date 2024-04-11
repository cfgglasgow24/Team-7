# pages/urls.py

from django.urls import path
from pages import views

urlpatterns = [
    path("", views.home, name='home'),
    path("filter/", views.filter, name='filter'),
    path("request/", views.request, name='request'),
    path("register_mentor/", views.register_mentor, name='register_mentor'),
    path("register_mentee/", views.register_mentee, name='register_mentee'),
    path('login/', views.login, name="login")
]