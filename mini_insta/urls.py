
# mini_insta/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

from .views import (
    ProfileListView,
    ProfileDetailView,
    CreatePostView,
    ShowPostView,
    ProfileFeedView,
    FollowersListView,
    FollowingListView,
    SearchView
)

urlpatterns = [
    path('', ProfileListView.as_view(), name='show_all_profiles'),
    path('my_profile/', views.MyProfileView.as_view(), name='my_profile'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='show_profile'),

    path('profile/<int:pk>/create_post/', CreatePostView.as_view(), name="create_post"),

    path('post/<int:pk>/', ShowPostView.as_view(), name='show_post'),

    path('profile/<int:pk>/feed/', ProfileFeedView.as_view(), name='profile_feed'),
    path('profile/<int:pk>/follow/', views.FollowView.as_view(), name='follow'),
    

    path('profile/<int:pk>/followers/', FollowersListView.as_view(), name='show_followers'),

    path('profile/<int:pk>/following/', FollowingListView.as_view(), name='show_following'),

    path('search/', SearchView.as_view(), name='search'),

    path(
        'logout_confirmation/',
        views.LogoutConfirmationView.as_view(),
        name='logout_confirmation'
    ),

    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='mini_insta/login.html'
        ),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(
            next_page='logout_confirmation'
        ),
        name='logout'
    ),
]