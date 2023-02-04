from rest_framework import serializers
from shop.models import Category, Product, ProductImages
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer
    product_images = ProductImagesSerializer
    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'qty', 'active', 'created_at', 'category', 'productImages' ]


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']

class UserSerializerWithToken(UserSerializer):
    access_token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'access_token']

    def get_access_token(self, user):
        token = RefreshToken.for_user(user)
        return str(token.access_token)