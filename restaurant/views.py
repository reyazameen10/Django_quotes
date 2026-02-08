from django.shortcuts import render
from django.http import HttpResponse
import random #added new changes for style and formatting
from datetime import datetime, timedelta

def main(request):
    return render(request, 'restaurant/main.html')

#order page
def order(request):

    specials = [
        ("Truffle Burger", 14.99),
        ("Spicy Ramen Bowl", 12.50),
        ("BBQ Chicken Pizza", 13.75),
        ("Lobster Roll", 18.00)
    ]

    daily_special = random.choice(specials)

    context = {
        "daily_special_name": daily_special[0],
        "daily_special_price": daily_special[1]
    }

    return render(request, 'restaurant/order.html', context)


#confirmation page
def confirmation(request):

    if request.method == "POST":

        prices = {
            "burger": 10,
            "pizza": 12,
            "salad": 8,
            "pasta": 11,
            "special": float(request.POST.get("special_price", 0))
        }

        ordered_items = []
        total = 0

        for item, price in prices.items():
            if request.POST.get(item):
                ordered_items.append(item)
                total += price

        ready_time = datetime.now() + timedelta(minutes=random.randint(30, 60))

        context = {
            "name": request.POST.get("name"),
            "phone": request.POST.get("phone"),
            "email": request.POST.get("email"),
            "instructions": request.POST.get("instructions"),
            "items": ordered_items,
            "total": total,
            "ready_time": ready_time.strftime("%I:%M %p")
        }
    return render(request, 'restaurant/confirmation.html', context)
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
        