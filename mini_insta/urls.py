#mini_insta/urls.py

from django.urls import path
from .views import ProfileListView, ProfileDetailView, CreatePostView, ShowPostView, ProfileFeedView, FollowersListView, FollowingListView, SearchView

urlpatterns = [
    path('', ProfileListView.as_view(), name='show_all_profiles'),
    path('<int:pk>/', ProfileDetailView.as_view(), name='show_profile'),
    path('profile/<int:pk>/create_post/', CreatePostView.as_view(), name="create_post"), #new url pattern for creating a new post
    path('post/<int:pk>/', ShowPostView.as_view(), name='show_post'), #new url pattern for showing a post detail page
    path('<int:pk>/feed/', ProfileFeedView.as_view(), name='profile_feed'),
    path('<int:pk>/followers/', FollowersListView.as_view(), name='show_followers'),
    path('<int:pk>/following/', FollowingListView.as_view(), name='show_following'),
    path('<int:pk>/search/', SearchView.as_view(), name='search'),
]
