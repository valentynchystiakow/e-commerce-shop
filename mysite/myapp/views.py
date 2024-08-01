# import libraries(modules)
from django.shortcuts import render
from django.http import HttpResponse

# import models
from .models import Product


# Create your views here.
# function that renders all products page
def index(request):
    # saves Product model objects in variable
    items = Product.objects.all()
    context = {'items': items}
    # renders index template
    return render(request, "myapp/index.html", context)


# function that renders product by it's id
def indexItem(request, my_id):
    # gets every product's object id and saves it in variable
    item = Product.objects.get(id=my_id)
    context = {
        'item': item
    }
    return render(request, "myapp/detail.html", context=context)
