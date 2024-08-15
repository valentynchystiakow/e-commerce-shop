# import libraries(modules)
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import NewUserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# import new user form
from .forms import NewUserForm


# Views

# function that registers new user
def register(request):
    # checks request method
    if request.method == "POST":
        form = NewUserForm(request.POST)
        # checks is user form is valid
        if form.is_valid():
            user = form.save()
            # logins created user
            login(request, user)
            # after logging redirects to main page
            return redirect("myapp:index")
    form = NewUserForm()
    context = {"form": form}
    return render(request, "users/register.html", context)


# Decorator which requires user to be logged
@login_required
# function that renders users profile page
def profile(request):
    return render(request, 'users/profile.html')


# function that shows seller profile
def seller_profile(request, id):
    # gets seller from User objects by id
    seller = User.objects.get(id=id)
    context = {
        'seller': seller
    }
    return render(request, 'users/sellerprofile.html', context)
