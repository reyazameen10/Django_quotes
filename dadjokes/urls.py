#dadjokes/ urls.py reyam/CS412

from django.urls import path
from . import views

#adding urls one by one

urlpatterns = [
    path('', views.random_view),
    path('random/', views.random_view),
    path('api', views.api_view, name='dadjokes-api'),
    path('jokes/', views.jokes_list),
    
  path('joke/<int:pk>/', views.joke_detail),
    path('pictures/', views.pictures_list),
    path('picture/<int:pk>/', views.joke_detail),
]