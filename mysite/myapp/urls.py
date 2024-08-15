# import libraries(modules)
from django.urls import path
# import views models
from myapp.views import add_item, update_item, ProductListView, ProductDetailView, ProductDeleteView


app_name = "myapp"

# myapp url pathes
urlpatterns = [
    # http://127.0.0.1:8000/myapp
    path('', ProductListView.as_view(), name='index'),
    # http://127.0.0.1:8000/myapp/4
    path("<int:pk>/", ProductDetailView.as_view(), name="detail"),
    # http://127.0.0.1:8000/myapp/additem
    path("additem/", add_item, name='add_item'),
    # http://127.0.0.1:8000/myapp/updateitem/1/
    path("updateitem/<int:my_id>/", update_item, name="update_item"),
    # http://127.0.0.1:8000/myapp/deleteitem
    path("deleteitem/<int:pk>/", ProductDeleteView.as_view(), name="delete_item")
]
