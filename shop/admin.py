from django.contrib import admin
from .models import Category, ProductImages, Product, Order, Shipping, OrderItem

# Register your models here.

admin.site.register(Category)
admin.site.register(ProductImages)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Shipping)
admin.site.register(OrderItem)
