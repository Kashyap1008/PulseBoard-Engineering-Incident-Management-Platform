from django.shortcuts import render



from rest_framework import generics 
from rest_framework.permissions import IsAuthenticated
from.permissions import IsOrganizationMember
from .models import Organization,OrganizationMembership,Team,TeamMembership
from .serializers import OrganizationSerializer,TeamSerializer

class OrganizationListCreateView(generics.ListCreateAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Organization.objects.filter(memberships__user = self.request.user)

    def perform_create(self, serializer):
        organization = serializer.save()
        OrganizationMembership.objects.create(user=self.request.user,
                                              organization=organization,
                                              role =OrganizationMembership.Role.OWNER)
        
class TeamListCreateView(generics.ListCreateAPIView):
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated,IsOrganizationMember]

    def get_queryset(self):
        return Team.objects.filter(memberships__user= self.request.user)

    