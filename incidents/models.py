from django.db import models
from django.conf import settings
from organizations.models import Team
# Create your models here.

class Incident(models.Model):
    class Meta:
        indexes = [
        models.Index(fields=["status"]),
        models.Index(fields=["severity"]),
        ]

    class Severity(models.TextChoices):
        SEV1 = "SEV1", "Critical"
        SEV2 = "SEV2", "High"
        SEV3 = "SEV3", "Medium"
        SEV4 = "SEV4", "Low"

    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        INVESTIGATING = "INVESTIGATING", "Investigating"
        MITIGATED = "MITIGATED", "Mitigated"
        RESOLVED = "RESOLVED", "Resolved"
        REOPENED = "REOPENED", "Reopened"

    team = models.ForeignKey(Team,on_delete=models.SET_NULL,null=True,blank=True,related_name='incidents')
    title = models.CharField(max_length=200)
    description = models.TextField()
    severity = models.CharField(max_length=4,choices=Severity.choices,default=Severity.SEV4)
    status = models.CharField(max_length=20,choices=Status.choices,default=Status.OPEN)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_incidents'
    )

    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_incidents'
    )
   

    started_at = models.DateTimeField(
        null=True,
        blank=True
    )

    resolved_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class IncidentEvent(models.Model):
    class EventType(models.TextChoices):
        CREATED = "CREATED", "Created"
        STATUS_CHANGED = "STATUS_CHANGED", "Status Changed"
        SEVERITY_CHANGED = "SEVERITY_CHANGED", "Severity Changed"
        ASSIGNED = "ASSIGNED", "Assigned"
        UNASSIGNED = "UNASSIGNED", "Unassigned"
        COMMENTED = "COMMENTED", "Commented"
        RESOLVED = "RESOLVED", "Resolved"
        REOPENED = "REOPENED", "Reopened"

    incident = models.ForeignKey(Incident,on_delete=models.CASCADE,related_name='events')
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='incident_events'
    )
    event_type = models.CharField(max_length=20,choices=EventType.choices)
    message = models.TextField()
    meta_data = models.JSONField(default = dict,blank = True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event_type} - {self.incident.title}"


class IncidentComment(models.Model):
    incident = models.ForeignKey(Incident,on_delete=models.CASCADE,related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,related_name='incident_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"comment by {self.author} on {self.incident.title}"


    
