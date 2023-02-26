from django.urls import path
from .views import getAllProducts, getAllCategories, MyTokenObtainPairView, registerUser, CreateOrder, GetAllOrdersByUser, UpdatePassword, ForgotPasswordView, ChangeForgotPassword

urlpatterns = [
    path('products/', getAllProducts.as_view()),
    path('categories/', getAllCategories.as_view()),
    path('create_order/',CreateOrder.as_view()),
    path('getAllOrders/', GetAllOrdersByUser.as_view()),

    # Authentication Urls
    path('accounts/login/', MyTokenObtainPairView.as_view()),
    path('accounts/register/', registerUser.as_view()),
    path('update_password/', UpdatePassword.as_view()),
    path('forgot_password/', ForgotPasswordView.as_view()),
    path('change_forgot_password/', ChangeForgotPassword.as_view()),

]