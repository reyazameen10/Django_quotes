#dadjokes_project/ dadjokes/ admin.py

from django.contrib import admin

# I will import the models here
from .models import Joke, Picture

admin.site.register(Joke)
admin.site.register(Picture)