# pages/urls.py

from django.urls import path
from pages import views

urlpatterns = [
    path("", views.home, name='home'),
    path("filter/", views.filter, name='filter'),
    path("request/", views.request, name='request'),
    path("cv/", views.cv, name='cv'),
    path("job_opportunities/", views.job_opportunities, name='job_opportunities'),
    path("login/", views.login, name='login'),
    path("mentee_view/", views.mentee_view, name='mentee_view'),
    path("mentor_view/", views.mentor_view, name='mentor_view'),
    path("mentorship/", views.mentorship, name='mentorship'),
    path("register_mentee/", views.register_mentee, name='register_mentee'),
    path("register_mentor/", views.register_mentor, name='register_mentor'),
    path("support/", views.support, name='support'),
]