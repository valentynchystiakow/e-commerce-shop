# import libraries(modules)
from django.http.response import HttpResponse as HttpResponse
import stripe
# import django libraries(modules)
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import stripe.checkout

# import models
from .models import Product, OrderDetail


# Create your views here.
# function that renders all products page with search form and pagination
def index(request):
    page_obj = items = Product.objects.all()

    item_name = request.GET.get("search")
    if item_name != "" and item_name is not None:
        page_obj = items.filter(name__icontains=item_name)

    paginator = Paginator(page_obj, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj}
    return render(request, "myapp/index.html", context)


# Class Based Product ListView
class ProductListView(ListView):
    model = Product
    template_name = 'myapp/index.html'
    context_object_name = 'items'
    paginate_by = 2

# Function Based Product Detail View
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

    # function that gets context data into template(myapp/detail.html)
    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        # saves publishable key from setting into context variable
        context["stripe_publishable_key"] = settings.STRIPE_PUBLISHABLE_KEY
        return context


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
    success_url = reverse_lazy("myapp:index")


# function that creates payment checkout session
@csrf_exempt
def create_checkout_session(request, id):
    product = get_object_or_404(Product, pk=id)

    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": product.name,
                    },
                    "unit_amount": int(product.price * 100),
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=request.build_absolute_uri(reverse("myapp:success"))
        + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse("myapp:failed")),
    )

    # OrderDetail.objects.create(
    #     customer_email=email,
    #     product=product, ......
    # )

    order = OrderDetail()
    order.product = product
    order.stripe_payment_intent = checkout_session["payment_intent"]
    order.amount = int(product.price * 100)
    order.save()

    # return JsonResponse({'data': checkout_session})
    return JsonResponse({"sessionId": checkout_session.id})


class PaymentSuccessView(TemplateView):
    template_name = "myapp/payment_success.html"

    def get(self, request, *args, **kwargs):
        session_id = request.GET.get("session_id")
        if session_id is None:
            return HttpResponseNotFound()

        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.retrieve(session_id)

        order = get_object_or_404(
            OrderDetail, stripe_payment_intent=session.payment_intent
        )
        order.has_paid = True
        order.save()
        return render(request, self.template_name)


class PaymentFailedView(TemplateView):
    template_name = "myapp/payment_failed.html"
