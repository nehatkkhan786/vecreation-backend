from django.urls import path
from .views import getAllProducts, getAllCategories, MyTokenObtainPairView, registerUser

urlpatterns = [
    path('products/', getAllProducts.as_view()),
    path('categories/', getAllCategories.as_view()),

    # Authentication Urls
    path('accounts/login/', MyTokenObtainPairView.as_view()),
    path('accounts/register/', registerUser.as_view())
]