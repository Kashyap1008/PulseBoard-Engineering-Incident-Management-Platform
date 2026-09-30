from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Incident,IncidentEvent,IncidentComment
from .permissions import IsIncidentOrganizationMember

from .serializers import IncidentSerializer

class IncidentListCreateView(generics.ListCreateAPIView):
    serializer_class = IncidentSerializer
    permission_classes = [IsAuthenticated,IsIncidentOrganizationMember]

    def get_queryset(self):
        return Incident.objects.filter(team__organization__memberships__user = self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by = self.request.user)

class IncidentDetailView(generics.RetrieveAPIView):
    serializer_class = IncidentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
            return Incident.objects.filter(team__organization__memberships__user = self.request.user)

