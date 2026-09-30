from .models import Incident
from rest_framework import serializers

class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = ['id',
                  'team',
                  'title',
                  'description',
                  'severity',
                  'status',
                  'created_by',
                  'assignee',
                  'started_at',
                  'resolved_at',
                  'created_at',
                  'updated_at']

        read_only_fields = ['id','created_by','started_at','assignee','created_at']

    
