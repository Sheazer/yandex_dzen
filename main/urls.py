from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CustomTokenObtainView, register

urlpatterns = [
    path("login/", CustomTokenObtainView.as_view(), name="login"),
    path('register/', register, name='register'),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
