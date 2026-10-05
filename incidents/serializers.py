from .models import Incident,IncidentEvent,IncidentComment
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
                  'tags',
                  'created_by',
                  'assignee',
                  'started_at',
                  'resolved_at',
                  'created_at',
                  'updated_at']

        read_only_fields = ['id','created_by','started_at','assignee','created_at']


class IncidentTranistionSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices= Incident.Status.choices)

class IncidentAssignmentSerializer(serializers.Serializer):
    assignee  = serializers.IntegerField(allow_null = True)

class IncidentTeamSerializer(serializers.Serializer):
    team = serializers.IntegerField()

class IncidentServeritySerializer(serializers.Serializer):
    severity = serializers.ChoiceField(choices=Incident.Severity.choices)

class IncidentEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncidentEvent
        fields = [
            "id",
            "incident",
            "actor",
            "event_type",
            "message",
            "meta_data",
            "created_at",
        ]
        read_only_fields = fields

class IncidentCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncidentComment
        fields = [
            "id",
            "incident",
            "author",
            "content",
            "created_at",
        ]

        read_only_fields = ["id","incident","author","created_at"]
    
