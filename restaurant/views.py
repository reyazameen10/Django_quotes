from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def show_menu(request):
    '''shows the menu page'''

    template_name = 'restaurant/form.html'
    return render(request, template_name)
    
def submit(request):
    '''process the menu submission, and generate a response'''

    template_name = "restaurant/confirmation.html"

    print(request.POST)
    #check if POST data was sent with HTTP POST message
    if request.method == "POST":
        #extract menu menu fields into variables
        name = request.POST['name']
        favorite_food = request.POST['food']

        context = {
            'name': name,
            'favorite_food': favorite_food,
        }

    return render(request, template_name=template_name, context=context)
        