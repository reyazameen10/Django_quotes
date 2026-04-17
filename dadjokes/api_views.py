#dadjokes / api_views.py/ reyam / CS412

import random 
from rest_framework.decorators import api_view

from rest_framework.response import Response
from .models import Joke, Picture

from .serializers import JokeSerializer, PictureSerializer

@api_view(['GET'])
def api_random_joke(request):
    joke = random.choice(Joke.objects.all())
    return Response(JokeSerializer(joke).data)


@api_view(['GET', 'POST'])
def api_jokes(request):
    if request.method == 'GET':
        jokes = Joke.objects.all()
        return Response(JokeSerializer(jokes, many=True).data)
    
    if request.method == 'POST':
        serializer = JokeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
@api_view(['GET'])
def api_joke_detail(request,pk):
    joke = Joke.objects.get(pk=pk)
    return Response(JokeSerializer(joke).data)
    
@api_view(['GET'])
def api_pictures(request):
    picture = Picture.objects.all()
    return Response(PictureSerializer(picture, many=True).data)
    
@api_view(['GET'])
def api_picture_detail(request, pk):
    picture = Picture.objects.get(pk=pk)
    return Response(PictureSerializer(picture).data)

@api_view(['GET'])
def api_random_picture(request):
    picture = random.choice(Picture.objects.all())
    return Response(PictureSerializer(picture).data)
