#dadjokes/ views.py reyam/ CS412

import random
from django.shortcuts import render, get_object_or_404
from .models import Joke, Picture
from django.http import JsonResponse # for api view, the error was that I forgot to import this module, so I added it here

def api_view(request):
    data = {"message": "Hello from API"}
    return JsonResponse(data)

#starting by random def
def random_view(request):
    joke = random.choice(Joke.objects.all())
    picture = random.choice(Picture.objects.all())
    return render(request, 'dadjokes/random.html', {
        'joke': joke,
        'picture':picture
    })


#jokes no image
def jokes_list(request):
    joke = Joke.objects.all()
    return render(request, 'dadjokes/jokes.html', {'jokes': joke})

#joke by it's PK
def joke_detail(request, pk):
    joke = get_object_or_404(Joke, pk=pk)
    return render(request, 'dadjokes/joke_detail.html', {'joke': joke})

#defive the pictures 
def pictures_list(request):
    pictures = Picture.objects.all()
    return render(request, 'dadjokes/pictures.html', {'pictures': pictures })

#pictrues by it's pk
def picture_detail(request, pk):
    picture = get_object_or_404(Picture, pk=pk)
    return render(request, 'dadjokes/picture_detail.html', {'picture': picture})