from .models import Organization,Service,Team,OrganizationMembership,TeamMembership 
from rest_framework import serializers


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta :
        model = Organization
        fields = ["id" , "name" , "created_at"]
        read_only_fields = ['id' , 'created_at']

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team 
        fields = ['id','name','organization','service','description','created_at']
        read_only_fields = ['id','created_at']

