from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView


class CustomTokenObtainView(TokenObtainPairView):
    permission_classes = [AllowAny]
