# import modules, libraries
from django.db import models
from django.contrib.auth.models import User


# Create your models here.


# Creates Profile model class from main Model class
class Profile(models.Model):
    # creates model's fields with their types
    # connects Profile table with User table
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, upload_to='_profile_images')
    contact_number = models.CharField(max_length=30, default="+7928123456789")

    # string representation of model
    def __str__(self):
        return self.user.username
