from django.db import models

# Create your models here.

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
    created_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.name

    

class Product(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    productImages = models.ForeignKey(ProductImages, on_delete=models.SET_NULL, null=True )
    price = models.IntegerField()
    qty = models.IntegerField(default=0)
    inActive = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}{ self.category}'

    