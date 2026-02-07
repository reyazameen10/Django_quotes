# restaurant/urls.py
# This file contains the URL patterns for the restaurant app. It maps URLs to views.

from django.urls import path
from django.conf import settings
from . import views 

app_name = 'restaurant' # new line to set the app name for namespacing

# URL patterns for the restaurant app
urlpatterns = [
    path("", views.show_menu, name="menu"), # Maps the URL
    path("submit/", views.submit, name="submit"), # Maps the URL for form submission
]
