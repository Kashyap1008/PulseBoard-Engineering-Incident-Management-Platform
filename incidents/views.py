from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Incident,IncidentEvent,IncidentComment
from .permissions import IsIncidentOrganizationMember,CanAssignIncident,CanChangeIncidentTeam,CanCommentOnIncident
from rest_framework.views import APIView
from rest_framework.response import Response
from audit.models import AuditLog
from .filters import IncidentFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from .serializers import IncidentSerializer,IncidentTranistionSerializer,IncidentAssignmentSerializer,IncidentTeamSerializer,IncidentServeritySerializer,IncidentEventSerializer,IncidentCommentSerializer

class IncidentListCreateView(generics.ListCreateAPIView):
    serializer_class = IncidentSerializer
    permission_classes = [IsAuthenticated,IsIncidentOrganizationMember]
    filter_backends = [DjangoFilterBackend,SearchFilter]
    filterset_class = IncidentFilter
    search_fields = [
        "title",
        "description"
    ]

    def get_queryset(self):
        return Incident.objects.filter(
            team__organization__memberships__user=self.request.user
        ).order_by("-created_at")
    def perform_create(self, serializer):
        incident = serializer.save(created_by = self.request.user)

        IncidentEvent.objects.create(
            incident=incident,
            actor = self.request.user,
            event_type = IncidentEvent.EventType.CREATED,
            message = "Incident Created",
            meta_data = {}
        )
        AuditLog.objects.create(
            actor =self.request.user,
            action = AuditLog.ACTION.INCIDENT_CREATED,
            target_type = "Incident",
            target_id = incident.id,
            message =  f"Incident {incident.title} was created by {self.request.user}'",
            meta_data = {}
        )

class IncidentDetailView(generics.RetrieveAPIView):
    serializer_class = IncidentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
            return Incident.objects.filter(team__organization__memberships__user = self.request.user)

    

class IncidentTransitionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request,pk):
        serializer = IncidentTranistionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        incident =  Incident.objects.get(pk=pk)    
        old_status = incident.status
        new_status = serializer.validated_data["status"]
        try:
            incident.change_status(new_status)
        except ValueError as e:
            return Response(
                {"detail":str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        IncidentEvent.objects.create(
            incident =  incident,
            actor = request.user,
            event_type  = IncidentEvent.EventType.STATUS_CHANGED,
            message = f"incident status changed from {old_status} to {new_status}",
            meta_data = {
                "old_status":old_status,
                "new_status":new_status
            }
        )
        AuditLog.objects.create(
                    actor =request.user,
                    action = AuditLog.ACTION.INCIDENT_STATUS_CHANGED,
                    target_type = "Incident",
                    target_id = incident.id,
                    message =  f"incident status changed from {old_status} to {new_status}",
                    meta_data = {
                        "old_status": old_status,
                        "new_status": new_status
                    }
                )


        return Response(
            {"detail":"incident status updated sucessfully . "},
            status=status.HTTP_200_OK
        )

class IncidentAssignmentView(APIView):
    permission_classes = [IsAuthenticated,CanAssignIncident]

    def post(self,request,pk):
        serializer = IncidentAssignmentSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        try:
            incident = Incident.objects.get(pk=pk)
        except Incident.DoesNotExist:
            return Response(
                {"detail": "Incident not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        self.check_object_permissions(request,incident)

        assignee_id = serializer.validated_data["assignee"]
        if assignee_id is None:
            old_assignee = incident.assignee_id
            incident.assignee = None
            incident.save(update_fields=["assignee","updated_at"])
            IncidentEvent.objects.create(
                incident = incident,
                actor=request.user,
                event_type=IncidentEvent.EventType.UNASSIGNED,
                message = "incident unassigned",
                meta_data = {}
                )
            AuditLog.objects.create(
                    actor =request.user,
                    action = AuditLog.ACTION.INCIDENT_UNASSIGNED,
                    target_type = "Incident",
                    target_id = incident.id,
                    message =  f"incident unassigned",
                    meta_data = {
                        "old_assignee": old_assignee,
                        "new_assignee": None
                    }
                )  
        else:
            old_assignee = incident.assignee
            if old_assignee is None:
                action = AuditLog.ACTION.INCIDENT_ASSIGNED
            else:
                action = AuditLog.ACTION.INCIDENT_ASSIGNEE_CHANGED
            incident.assignee_id = assignee_id
            incident.save(update_fields=["assignee","updated_at"])
            incident.refresh_from_db() 
            IncidentEvent.objects.create(
                incident = incident,
                actor=request.user,
                event_type=IncidentEvent.EventType.ASSIGNED,
                message = f"incident assigned to user {incident.assignee.name}",
                meta_data = {"assignee": assignee_id}
                )
            AuditLog.objects.create(
                actor =request.user,
                action = action,
                target_type = "Incident",
                target_id = incident.id,
                message =  f"incident assigned to user {incident.assignee.name}",
                meta_data = {"assignee": assignee_id}
            )
        return Response(
            IncidentSerializer(incident).data,
            status=status.HTTP_200_OK
        )

class IncidentTeamView(APIView):
    permission_classes = [IsAuthenticated,CanChangeIncidentTeam]
    def patch(self,request,pk):
        serializer = IncidentTeamSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        try:
            incident = Incident.objects.get(pk=pk)
        except Incident.DoesNotExist:
            return Response(
                {"detail":"incident not found"},
                status=status.HTTP_404_NOT_FOUND
            )   

        self.check_object_permissions(request,incident)

        old_team = incident.team
        new_team = serializer.validated_data["team"]

        incident.team_id =new_team
        incident.save(update_fields=["team","updated_at"])

        IncidentEvent.objects.create(
            incident=incident,
            actor = request.user,
            event_type = IncidentEvent.EventType.TEAM_CHANGED,
            message = f"Incident team changed from {old_team.name} to {incident.team.name}",
            meta_data = {
                "old_team": old_team.id,
                "new_team": new_team
            }

        )
        AuditLog.objects.create(
            actor =request.user,
            action = AuditLog.ACTION.INCIDENT_TEAM_CHANGED,
            target_type = "Incident",
            target_id = incident.id,
            message = f"Incident team changed from {old_team.name} to {incident.team.name}",
            meta_data = {
                "old_team": old_team.id,
                "new_team": new_team
            }
        )

        return Response(
            IncidentSerializer(incident).data,
            status=status.HTTP_200_OK
        )

class IncidentSeverityView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self,request,pk):
        serializer = IncidentServeritySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            incident = Incident.objects.get(pk=pk)
        except Incident.DoesNotExist:
            return Response(
                {"detai":"incident Not Found"},
                status=status.HTTP_404_NOT_FOUND
            )

        old_severity = incident.severity
        new_severity = serializer.validated_data["severity"]

        if old_severity==new_severity:
            return Response(
                {"detail":"incident already has this severity"},
                status=status.HTTP_400_BAD_REQUEST
            )
        incident.severity = new_severity
        incident.save(update_fields=["severity","updated_at"])

        IncidentEvent.objects.create(
                incident=incident,
                actor = request.user,
                event_type = IncidentEvent.EventType.SEVERITY_CHANGED,
                message = f"Incident severity changed from {old_severity} to {incident.severity}",
                meta_data = {
                    "old_severity": old_severity,
                    "new_severity": new_severity
                }
                )
        AuditLog.objects.create(
                    actor = request.user,
                    action = AuditLog.ACTION.INCIDENT_SEVERITY_CHANGED,
                    target_type = "Incident",
                    target_id = incident.id,
                    message =  f"Incident severity changed from {old_severity} to {incident.severity}",
                    meta_data = {
                        "old_severity": old_severity,
                        "new_severity": new_severity
                    }
                )

        return Response(
            IncidentSerializer(incident).data,
            status=status.HTTP_200_OK
        )

class IncidentTimelineView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,pk):
        try:
            incident = Incident.objects.get(pk=pk)
        except Incident.DoesNotExist:
            return Response(
                {"detail" : "Incident Not Found."},
                status=status.HTTP_404_NOT_FOUND
            )

        events = IncidentEvent.objects.filter(incident=incident).order_by("-created_at")

        serializer = IncidentEventSerializer(events,many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

class IncidentCommentCreateView(APIView):
    permission_classes = [IsAuthenticated,CanCommentOnIncident]
    def get(self,request,pk):
        try:
            incident = Incident.objects.get(pk=pk)
        except Incident.DoesNotExist:
            return Response(
                {"detail":"Incident Not Found"},
                status=status.HTTP_404_NOT_FOUND
            )
        self.check_object_permissions(request,incident)
        comments = IncidentComment.objects.filter(incident=incident).order_by("created_at")
        serializer = IncidentCommentSerializer(comments,many = True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )       

    def post(self,request,pk):
        try:
            incident = Incident.objects.get(pk=pk)
        except Incident.DoesNotExist:
            return Response(
                {"detail":"Incident Not Found"},
                status=status.HTTP_404_NOT_FOUND
            )
        self.check_object_permissions(request,incident)
        serializer = IncidentCommentSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        comment = serializer.save(incident=incident,author=request.user)
        return Response(
            IncidentCommentSerializer(comment).data,
            status=status.HTTP_201_CREATED
        )






            

