#mini_insta/urls.py

from django.urls import path
from .views import ProfileListView, ProfileDetailView, CreatePostView, ShowPostView

urlpatterns = [
    path('', ProfileListView.as_view(), name='show_all_profiles'),
    path('<int:pk>/', ProfileDetailView.as_view(), name='show_profile'),
    path('profile/<int:pk>/create_post/', CreatePostView.as_view(), name="create_post"), #new url pattern for creating a new post
    path('post/<int:pk>/', ShowPostView.as_view(), name='show_post') #new url pattern for showing a post detail page
    
]
