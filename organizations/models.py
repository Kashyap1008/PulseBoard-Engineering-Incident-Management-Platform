from django.db import models
from django.conf import settings


# Create your models here.

class Organization(models.Model):
    name = models.CharField(max_length=150,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Service(models.Model):

    class Importance(models.IntegerChoices):
        LOW = 1, "Low"
        MEDIUM = 2, "Medium"
        HIGH = 3, "High"
        CRITICAL = 4, "Critical"

    name = models.CharField(max_length=100)

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="services"
    )

    description = models.TextField()

    importance = models.IntegerField(
        choices=Importance.choices,
        default=Importance.LOW
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Team(models.Model):

    name = models.CharField(max_length=100)

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="teams"
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="teams"
    )

    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class TeamMembership(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="team_memberships"
    )

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="memberships"
    )

    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [ models.UniqueConstraint(fields=['user','team'],name = 'unique_user_team') ]

    def __str__(self):
        return f"{self.user.name} - {self.team.name}"


