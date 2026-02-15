from django.db import models

class Profile(models.Model):
    username = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=100)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True, max_length=500)
    join_date = models.DateField()
    
    def __str__(self):
        return f'{self.username}'
