from django.db import models 
from django.conf import settings

# Create your models here.

class AuditLog(models.Model):
    class ACTION(models.TextChoices):
        ORGANIZATION_CREATED = 'ORGANIZATION_CREATED' , 'Organization created'
        ORGANIZATION_MEMBER_ADDED = 'ORGANIZATION_MEMBER_ADDED','Organization Member Added'
        ORGANIZATION_MEMBER_REMOVED = 'ORGANIZATION_MEMBER_REMOVED','Organization Member Removed'
        ORGANIZATION_MEMBER_ROLE_CHANGED = 'ORGANIZATION_MEMBER_ROLE_CHANGED','Organization member role changed'
        USER_CREATED  = 'USER_CREATED','User Created'
        USER_DEACTIVATED = 'USER_DEACTIVATED','User Deacticated'
        SERVICE_CREATED = 'SERVICE_CREATED','Service created'
        SERVICE_DELETED = 'SERVICE_DELETED', 'Service Deleted'
        TEAM_CREATED = 'TEAM_CREATED', 'Team Created'
        TEAM_DELETED = 'TEAM_DELETED', 'Team Deleted'
        TEAM_MEMBER_ADDED = 'TEAM_MEMBER_ADDED', 'Team Member Added'
        TEAM_MEMBER_REMOVED = 'TEAM_MEMBER_REMOVED', 'Team Member Removed'
        INCIDENT_CREATED = 'INCIDENT_CREATED','Incident Created'
        INCIDENT_STATUS_CHANGED = 'INCIDENT_STATUS_CHANGED','Incident Status Changed'
        INCIDENT_SEVERITY_CHANGED = 'INCIDENT_SEVERITY_CHANGED', 'Incident Severity Changed'
        INCIDENT_ASSIGNED = 'INCIDENT_ASSIGNED', 'Incident Assigned'
        INCIDENT_UNASSIGNED = 'INCIDENT_UNASSIGNED','Incident Unassigned'
        INCIDENT_ASSIGNEE_CHANGED = 'INCIDENT_ASSIGNEE_CHANGED','Incident Assignee Changed'
        INCIDENT_TEAM_CHANGED = 'INCIDENT_TEAM_CHANGED', 'Incident Team Changed'


    actor =  models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.Prefetch,related_name='audit_logs')
    action = models.CharField(max_length=100,choices=ACTION.choices)
    target_type = models.CharField(max_length=100)
    target_id = models.PositiveIntegerField()
    message = models.TextField()
    meta_data = models.JSONField(
        default=dict,
        blank = True
    )
    created_at = models.DateTimeField(auto_now_add=True)


