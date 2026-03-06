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
        return self.username

    # Followers
    def get_followers(self):
        follows = Follow.objects.filter(profile=self)
        return [f.follower_profile for f in follows]

    def get_num_followers(self):
        return Follow.objects.filter(profile=self).count()

# Following
    def get_following(self):
        follows = Follow.objects.filter(follower_profile=self)
        return [f.profile for f in follows]

    def get_num_following(self):
        return Follow.objects.filter(follower_profile=self).count()


# Post Model
class Post(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    image_url = models.URLField()
    caption = models.TextField(blank=True, max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.profile.username}"

    def get_absolute_url(self):
        return reverse('post', kwargs={'pk': self.pk})


# Follow Model 
class Follow(models.Model):
    profile = models.ForeignKey(
        Profile,
        related_name='followers',
        on_delete=models.CASCADE
    )
    follower_profile = models.ForeignKey(
        Profile,
        related_name='following',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.follower_profile} follows {self.profile}"