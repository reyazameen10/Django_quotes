# mini_insta/models.py

from django.db import models
from django.urls import reverse

class Profile(models.Model):
    username = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=100)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True, max_length=500)
    join_date = models.DateField()
    
    def __str__(self):
        return f'{self.username}'

        # The Post model represents a post made by a user (Profile). Each post has an image URL, an optional caption, and a timestamp for when it was created. The profile field is a foreign key that links the post to the Profile that created it. The related_name='posts' allows us to access all posts of a profile using profile.posts.

class Post(models.Model):  
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    image_url = models.URLField()
    caption = models.TextField(blank=True, max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.profile.username}"

        def get_absolute_url(self):
            '''Return the URL to access a detail record for this post.'''
            return reverse('post', kwargs={'pk': self.pk})
