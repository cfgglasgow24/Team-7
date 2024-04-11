# pages/urls.py

from django.urls import path
from pages import views

app_name = 'CodeDivisionMentoring'

urlpatterns = [
    path("", views.home, name='home'),
    path("", views.addEvent, name='addEvent'),
    path("", views.cv, name='cv'),
    path("", views.job_opportunities, name='job_opportunities'),
    path("", views.support, name='support'),
    path("", views.mentorship, name='mentorship'),   
]