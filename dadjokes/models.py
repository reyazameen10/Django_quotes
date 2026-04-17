#dadjokes/ models.py adding

from django.db import models

#this class is for the first section (joke)
class Joke(models.Model):
    text = models.TextField() 
    contributor = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]
    
#this section for the picture 

class Picture(models.Model):
    image_url = models.URLField()
    contributor = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    #define the model
    def __str__(self):
        return self.image_url
