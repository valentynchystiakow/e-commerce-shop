# import libraries(modules)
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
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


# Class Based Product ListView
class ProductListView(ListView):
    model = Product
    template_name = 'myapp/index.html'
    context_object_name = 'items'


# function that renders product by it's id
# def indexItem(request, my_id):
    # gets every product's object id and saves it in variable
    #   item = Product.objects.get(id=my_id)
  #  context = {
   #     'item': item
    # }
    # return render(request, "myapp/detail.html", context=context)


# Class Based Product Detail View
class ProductDetailView(DetailView):
    model = Product
    template_name = "myapp/detail.html"
    context_object_name = "item"
    pk_url_kwarg = "pk"


# decorator that requires user to be loggen in order to add items
@login_required
# function that ads item to database
def add_item(request):
    # checks if request method = Post
    if request.method == "POST":
        # saves item form in variables
        name = request.POST.get("name")
        price = request.POST.get("price")
        description = request.POST.get("description")
        image = request.FILES['upload']
        seller = request.user
        item = Product(name=name, price=price,
                       description=description, image=image, seller=seller)
        item.save()
    return render(request, "myapp/additem.html")


# function that updates items in database
def update_item(request, my_id):
    # updates item by its id
    item = Product.objects.get(id=my_id)
    # checks if request methos is post
    if request.method == "POST":
        # saves item form in variables
        item.name = request.POST.get("name")
        item.price = request.POST.get("price")
        item.description = request.POST.get("description")
        item.image = request.FILES.get('upload', item.image)
        item.save()
        # redirects to main page
        return redirect("/myapp/")
    context = {"item": item}
    return render(request, "myapp/updateitem.html", context)


# function that deletes items in database
def delete_item(request, my_id):
    # deletes item by its id
    item = Product.objects.get(id=my_id)
    # checks if request methos is post
    if request.method == "POST":
        # saves item form in variables
        item.delete()
        # redirects to main page
        return redirect("/myapp/")
    context = {"item": item}
    return render(request, "myapp/deleteitem.html", context)


class ProductDeleteView(DeleteView):
    model = Product
    # url on which user will be redirect after deleting item
    success_url = reverse_lazy("myapp:index")
