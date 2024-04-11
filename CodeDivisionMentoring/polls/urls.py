from django.urls import path, re_path
from polls.views import index

# url patterns
urlpatterns = [
     path("", 
         index, 
         name="main"),
     path("index", 
          index, 
          name="index"),
]
