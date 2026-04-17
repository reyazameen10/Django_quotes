

#dadjokes / api_urls.py reyam/CS412

from django.urls import path
from . import api_views

urlpatterns = [
    path('', api_views.api_random_joke),
    path('random/', api_views.api_random_joke),
    path('jokes/', api_views.api_jokes),
    path('joke/<int:pk>/', api_views.api_joke_detail),
    path('pictures/', api_views.api_pictures),
    path('picture/<int:pk>/', api_views.api_picture_detail),
    path('random_picture/', api_views.api_random_picture),
]

