# import libraries(modules)
from django.db import models


# Create your models here.
# Creates Product model class from main Model class
class Product(models.Model):
    # creates model's fields with their types
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.CharField(max_length=200)
    image = models.ImageField(blank=True, upload_to='images')

    # string representation of the object(class)
    def __str__(self):
        return self.name
