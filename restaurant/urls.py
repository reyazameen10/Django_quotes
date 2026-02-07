# restaurant/urls.py
# This file contains the URL patterns for the restaurant app. It maps URLs to views.

from django.urls import path
from django.conf import settings
from . import views 

# URL patterns for the restaurant app
urlpatterns = [
    path(r'', views.show_menu, name='show_menu'), # Maps the URL
    path(r'submit/', views.submit, name='submit'), # Maps the URL for form submission
]
