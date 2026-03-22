#reyam/ voter_analytics / urls.py

from django.urls import path
from . import views
from .views import VoterListView, VoterDetailView, GraphView

app_name = 'voter_analytics'

urlpatterns = [
    path('', VoterListView.as_view(), name='voters'),
    path('voter/<int:pk>/', VoterDetailView.as_view(), name='voter'),
    path('graphs/', GraphView.as_view(), name='graphs'), #graph
]