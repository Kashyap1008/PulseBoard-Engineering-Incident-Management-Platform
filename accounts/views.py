from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer,ProfileSerializer
from .models import User
from rest_framework.permissions import IsAuthenticated


# Create your views here.


class RegisterView(generics.CreateAPIView):
    queryset =  User.objects.all()
    permission_classes =  [AllowAny]
    serializer_class = RegisterSerializer

class ProfileAPIView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


