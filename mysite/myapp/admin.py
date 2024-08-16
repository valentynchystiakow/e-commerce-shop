# import libraries(modules)
from django.contrib import admin
from .models import Product


# changes site attributes on admin page
admin.site.site_header = "My Django Shop"
admin.site.site_title = "Title of Django"
admin.site.index_title = "My admin"


# Product Admin class which extends from main ModelAdmin class
class ProductAdmin(admin.ModelAdmin):
    # creates Product table poles in admin page
    list_display = ("name", 'price', 'description',)
    # ads search_fields
    search_fields = ("description",)
    # ads new actions to product
    actions = ('make_zero',)
    # list of poles admin can edit
    list_editable = ("price", "description",)

    # function that resets action's price

    def make_zero(self, request, queryset,):
        queryset.update(price=0)


# Registers  models
admin.site.register(Product, ProductAdmin)
