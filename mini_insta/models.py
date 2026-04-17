# mini_insta/models.py

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    display_name = models.CharField(max_length=100)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True, max_length=500)
    join_date = models.DateField(auto_now_add=True)

    def get_following(self):
        return self.following.all()
    
    def get_followers(self):
        return self.followers.all()
    def __str__(self):
        return self.user.username


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
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="posts")
    image = models.URLField(blank=True)
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.profile.user.username}"

    def get_absolute_url(self):
        return reverse('post', kwargs={'pk': self.pk})
    
    class Meta:
        ordering = ['-created_at'] 



    
class Like(models.Model):

    post = models.ForeignKey(
        Post,
        related_name="likes",
        on_delete=models.CASCADE
    )

    profile = models.ForeignKey(
        Profile,
        related_name="liked_posts",
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile} likes {self.post}"
    
#the creat profile was not working so I added this part

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)