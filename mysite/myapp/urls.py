# import libraries(modules)
from django.urls import path
# import views models
from myapp.views import index, indexItem


app_name = "myapp"

# myapp url pathes
urlpatterns = [
    # http://127.0.0.1:8000/myapp
    path('', index),
    # path for every product - by it's id
    # http://127.0.0.1:8000/myapp
    path('<int:my_id>/', indexItem, name='detail'),

]
