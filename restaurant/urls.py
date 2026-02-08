# restaurant/urls.py
# This file contains the URL patterns for the restaurant app. It maps URLs to views.

from django.urls import path
from django.conf import settings
from . import views 

app_name = 'restaurant' # new line to set the app name for namespacing

# URL patterns for the restaurant app
urlpatterns = [
    path("", views.order, name="order"), # Maps the URL
    path("submit/", views.submit, name="submit"), # Maps the URL
    path('main/', views.main, name='main'),
    path('order/', views.order, name='order'),
    path('confirmation/', views.confirmation, name='confirmation'),
]

#creating home page