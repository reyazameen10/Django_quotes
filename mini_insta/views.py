# mini_insta/views.py

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile


class ProfileListView(ListView):
    '''Define a view to show all the profiles.'''
    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = 'profiles'


class ProfileDetailView(DetailView):
    '''Define a view to show one profile.'''
    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'
