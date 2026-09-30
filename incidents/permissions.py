from rest_framework.permissions import BasePermission
from organizations.models import Team 


class IsIncidentOrganizationMember(BasePermission):
    def has_permission(self, request, view):
        team_id = request.data.get("team")

        if request.method == 'GET':
            return True

        if not team_id:
            return False

        return Team.objects.filter(
            id=team_id,
            organization__memberships__user=request.user
        ).exists()