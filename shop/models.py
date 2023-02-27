from ast import mod
from distutils.command.upload import upload
from itertools import product
from tkinter.tix import IMAGE
from unicodedata import decimal
from django.db import models
import datetime
from django.contrib.auth.models import User
from .task import generate_image_hash
import blurhash
from PIL import Image
import numpy
import io
import base64

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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProductImages(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to=product_image_path)
    imgHash = models.CharField(max_length=14, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    # def save(self, *args, **kwargs):
    #     print('save method called')
    #     if not self.imgHash: 
    #         with self.image.open() as image_file:
    #             hash = blurhash.encode(image_file, x_components=4, y_components=3)
    #             self.imgHash = hash 
    #             super().save(*args, **kwargs) 
    #     else:
    #         super().save(*args, **kwargs) 
    
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
    customId = models.CharField(max_length=255,default='WEB-00001', blank=True, null=True )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    totalPrice = models.IntegerField()
    status = models.CharField(max_length=50, choices=ORDER_STATUS, blank=True, null=True)
    isPaid= models.BooleanField(default=False)
    transactionId = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        ordering = ['-created_at']


    def save(self, *args, **kwargs):
        if not self.pk:
            last_order = Order.objects.all().order_by('id').last()
            if last_order:
                last_custom_id = int(last_order.customId.split('-')[-1])
            else:
                last_custom_id = 0
            self.customId = 'WEB-{:05}'.format(last_custom_id + 1)
        
        # Need to Be Done
        if not self.status:
            print('New Order Has Been Placed')
        else:
            print(self.status[0])
        # End Need to be done

        super().save(*args, **kwargs)

    def __str__(self):
        return self.customId

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
    first_name = models.CharField(max_length=200, blank=True, null=True)
    lastName = models.CharField(max_length=200, blank=True, null=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    address = models.TextField()
    city =models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='India', blank=True, null=True)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return str(self.order.id)
        





