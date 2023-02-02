from django.contrib import admin
from .models import Category, ProductImages, Product

# Register your models here.

admin.site.register(Category)
admin.site.register(ProductImages)
admin.site.register(Product)
