from dataclasses import fields
from rest_framework import serializers
from shop.models import Category, Product, ProductImages, OrderItem, Shipping, Order
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import request


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request:
            representation['icon_url'] = request.build_absolute_uri(instance.icon.url)
        return representation


class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request:
            representation['image_url'] = request.build_absolute_uri(instance.image.url)
        return representation


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    productImages = ProductImagesSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'qty', 'active',
                  'created_at', 'shortDescription', 'category', 'productImages']


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


class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    orderItems = serializers.SerializerMethodField(read_only=True)
    shiping = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Order
        fields = '__all__'

    def get_orderItems(self, obj):
        items = obj.orderitem_set.all()
        serializers = OrderItemsSerializer(items, many=True)
        return serializers.data
    
    def get_shiping(self, obj):
        try:
            address = ShippingSerializer(obj.shiping, many=False).data
        except:
            address = False    
        return address
    
    def get_user(self, obj):
        user = obj.user
        serializer = UserSerializer(user, many=False)
        return serializer.data

