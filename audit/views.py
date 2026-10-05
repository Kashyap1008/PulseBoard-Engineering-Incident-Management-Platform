from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from .models import AuditLog
from .serializers import AuditLogSerializer
# Create your views here.

class AuditLogApiView(generics.ListAPIView):
    serializer_class = AuditLogSerializer
    permission_classes=[IsAdminUser]

    def get_queryset(self):
        return AuditLog.objects.all().order_by('created_at')
    

