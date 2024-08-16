# import libraries(modules)
from django.urls import path
# import views models
from myapp.views import index, add_item, update_item, ProductDetailView, ProductDeleteView,  PaymentSuccessView, PaymentFailedView, create_checkout_session


app_name = "myapp"

# myapp url pathes
urlpatterns = [
    # http://127.0.0.1:8000/myapp
    path('', index, name='index'),
    # http://127.0.0.1:8000/myapp/1
    path("<int:pk>/", ProductDetailView.as_view(), name="detail"),
    # http://127.0.0.1:8000/myapp/additem
    path("additem/", add_item, name='add_item'),
    # http://127.0.0.1:8000/myapp/updateitem/1/
    path("updateitem/<int:my_id>/", update_item, name="update_item"),
    # http://127.0.0.1:8000/myapp/deleteitem
    path("deleteitem/<int:pk>/", ProductDeleteView.as_view(), name="delete_item"),
    # http://127.0.0.1:8000/myapp/success
    path("success/", PaymentSuccessView.as_view(), name="success"),
    # http://127.0.0.1:8000/myapp/failed
    path("failed/", PaymentFailedView.as_view(), name="failed"),
    # http://127.0.0.1:8000/myapp/api/checkout-session/1
    path("api/checkout-session/<int:id>/",
         create_checkout_session, name="api_checkout_session"),
]
