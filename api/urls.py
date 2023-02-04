from django.urls import path
from .views import getAllProducts, getAllCategories, MyTokenObtainPairView

urlpatterns = [
    path('products/', getAllProducts.as_view()),
    path('categories/', getAllCategories.as_view()),

    # Authentication Urls
    path('accounts/login', MyTokenObtainPairView.as_view()),
]