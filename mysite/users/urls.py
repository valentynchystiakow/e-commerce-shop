# import libraries(modules)
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
# import views models
from .views import register, profile, seller_profile


app_name = "users"

# users url pathes
urlpatterns = [
    # http://127.0.0.1:8000/users/register/
    path('register/', register, name='register'),
    # http://127.0.0.1:8000/users/login/
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    # http://127.0.0.1:8000/users/logout/
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    # http://127.0.0.1:8000/users/profile/
    path('profile/', profile, name='profile'),
    # http://127.0.0.1:8000/users/sellerprofile/
    path('sellerprofile/<int:id>/', seller_profile, name='sellerprofile'),
]
