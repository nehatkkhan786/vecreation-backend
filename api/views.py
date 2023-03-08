from django.shortcuts import render
from .serializers import ProductSerializer, CategorySerializer, UserSerializer, UserSerializerWithToken, OrderSerializer
from shop.models import Product, Category, ProductImages, Order, Shipping, OrderItem, Contact
from accounts.models import PasswordResetToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
import random, string
from rest_framework.exceptions import ValidationError
from django.template.loader import render_to_string
from .whatsappHelper import sendMessage






from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

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

        orderUrl = f'https://vecreation.in/order_detail/{order.id}'
        message = render_to_string('Order_Confirm.html',{'name':user.first_name, 'orderId':order.customId, 'orderUrl':orderUrl})
        send_mail(
            subject="Order Confirmation Email",
            message='Order Confirmation Email',
            html_message=message,
            recipient_list=[user.email],
            from_email= 'info@vecreation.in',
        )
        

            
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data,  status=status.HTTP_200_OK)


class GetAllOrdersByUser(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request,  *args, **kwargs):
        user = request.user 
        order = user.order_set.all()
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)

       
class UpdatePassword(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data

        if data['password'] != data['confirmPassword']:
            return Response({'message':'Password Does not Match'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        else:
            user.set_password(data['password'])
            user.save()
            return Response({'message':'Password Successfully Updated'}, status=status.HTTP_200_OK)



class ForgotPasswordView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data 
        email = data['email']
        try:
            user = User.objects.get(email=email)
        except:
           raise ValidationError('User does not exist')
        token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _i in range(12))
        PasswordResetToken.objects.create(
            email=email,
            token = token
        )

        current_site = get_current_site(request)
        password_reset_url = f'https://vecreation.in/change_forgot_password/{token}'
        message = render_to_string('password_reset_email.html',{'email':email, 'token':token, 'user':user, 'password_reset_url':password_reset_url} )

        send_mail(
            subject="Password Reset Link",
            message='Password Reset Link',
            html_message=message,
            recipient_list=[email],
            from_email= 'info@vecreation.in',
        )
        print('email send')

        return Response({'message':'Reset Password Link Successfully Send.'}, status = status.HTTP_200_OK)

class ChangeForgotPassword(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        if data['password'] != data['confirmPassword']:
            raise ValidationError('Password doest not matched')
        reset_token = PasswordResetToken.objects.filter(token=data['token']).first()
        if not reset_token:
            raise  ValidationError('Invalid Link')
        user = User.objects.filter(email=reset_token.email).first()
        if not user:
            raise  ValidationError('No User Found')
        
        user.set_password(data['password'])
        user.save()
        reset_token.delete()
        return Response({'message':'Password Successfully Changed'}, status = status.HTTP_200_OK)

class ContactView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            # creata a contact model 
            contact = Contact.objects.create(
                name = data['name'],
                email= data['email'],
                phone= data['phone'],
                message = data['message'],
            )
        except:
            raise ValidationError('Something went Wrong!')
        return Response({'message':'Contact Successfully Created'}, status = status.HTTP_200_OK)
        

