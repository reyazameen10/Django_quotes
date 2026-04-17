#dadjokes/serializers.py this is manage REST API

from rest_framework import serializers
from .models import Joke, Picture


#we will add the class for each 
class JokeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Joke
        fields = '__all__'


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture 
        fields = '__all__'