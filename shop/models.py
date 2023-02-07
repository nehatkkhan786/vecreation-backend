from distutils.command.upload import upload
from itertools import product
from unicodedata import decimal
from django.db import models
import datetime
from django.contrib.auth.models import User


# Create your models here.




ORDER_STATUS = (
    ('order_confirmed', 'Order Confirmed'),
    ('processing', 'Processing'),
    ('dispatched', 'Dispatched'),
    ('delivered', 'Delivered'), 
    ('returned', 'Returned'), 
    ('cancelled', 'Cancelled'), 
    ('refunded', 'Refunded'), 
)



def product_image_path(instance, filename):
    return 'products/{0}/{1}'.format(instance.name, filename)


class Category(models.Model):
    name = models.CharField(max_length=100)
    icon= models.ImageField(upload_to='CategoryIcons/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProductImages(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to=product_image_path)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    productImages = models.ManyToManyField(ProductImages)
    price = models.IntegerField()
    qty = models.IntegerField(default=0)
    shortDescription = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}{ self.category}'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    totalPrice = models.IntegerField()
    status = models.CharField(max_length=50, choices=ORDER_STATUS, blank=True, null=True)
    isPaid= models.BooleanField(default=False)
    transactionId = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.id

class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255)
    qty = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=7)
    created_at = models.DateTimeField(default=datetime.datetime.now)


    def __str__(self):
        return str(self.order.id)
    
    class Meta:
        ordering = ['-created_at']



class Shipping(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    address = models.TextField()
    city =models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return str(self.order.id)
        





