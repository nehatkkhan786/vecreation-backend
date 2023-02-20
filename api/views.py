from django.shortcuts import render
from .serializers import ProductSerializer, CategorySerializer, UserSerializer, UserSerializerWithToken, OrderSerializer
from shop.models import Product, Category, ProductImages, Order, Shipping, OrderItem
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated



from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.

class getAllProducts(APIView):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True , context={'request':request})
        return Response(serializer.data, status = status.HTTP_200_OK )

class getAllCategories(APIView):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories,context={'request':request},  many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)

class MytokenPairViewSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data

        for k, v in serializer.items():
            data[k] = v
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MytokenPairViewSerializer


class registerUser(APIView):
    def post(self, request, *args, **kwargs):  
        try:
            data = request.data
            if data['password'] == data['confirmPassword']:
                if User.objects.filter(username=data['email']).exists():
                    return Response({'Message':'User Already Exists'}, status= status.HTTP_400_BAD_REQUEST)
                else:
                    newUser = User.objects.create(
                        first_name = data['firstName'],
                        last_name = data['lastName'],
                        email = data['email'],
                        password = make_password(data['password'])
                    )
                    return Response({'message':'Account Created successfully'}, status = status.HTTP_200_OK)

            else:
                return Response({'message':'Password Doesnt Match'})
        except:
            print('Not Working')
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class CreateOrder(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        shippingAddress = request.data['shippingAddress']
        orderItems = data['cartItems']
        if orderItems and len(orderItems) < 1:
            return Response({'message':'No Order Items'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Create Order
            order = Order.objects.create(
                user = user,
                totalPrice = data['totalPrice'],
            )
            # Create Shipping For the Order

            shipping = Shipping.objects.create(
                order= order,
                first_name = shippingAddress['firstName'],
                lastName = shippingAddress['lastName'],
                address = shippingAddress['address'],
                city= shippingAddress['city'],
                state = shippingAddress['state'],
                zipcode = shippingAddress['zipcode'],
                phone_number = shippingAddress['phone']
            )

            # create Order Items
            for i in orderItems:
                product = Product.objects.get(id = i['id'])
                
                item = OrderItem.objects.create(
                    user = user,
                    order = order,
                    product = product,
                    name= product.title,
                    qty = i['qty'],
                    price = product.price,        
                )
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data,  status=status.HTTP_200_OK)
       
