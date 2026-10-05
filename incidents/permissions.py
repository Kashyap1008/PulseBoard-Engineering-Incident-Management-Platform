from rest_framework.permissions import BasePermission
from organizations.models import Team ,OrganizationMembership,ServiceMembership



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

class CanAssignIncident(BasePermission):
    ASSIGNMENT_LEVELS ={
        OrganizationMembership.Role.OWNER :4,
        OrganizationMembership.Role.ADMIN :4,
        OrganizationMembership.Role.SERVICE_MANAGER :4,
        OrganizationMembership.Role.TEAM_MANAGER :3,
        OrganizationMembership.Role.SENIOR_ENGINEER :2,
        OrganizationMembership.Role.JUNIOR_ENGINEER :1,
    }
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if obj.team is None:
            return False
        
        assignee_id = request.data.get("assignee")

        if assignee_id is None:
            if obj.assignee is None:
                return False

            # Assignee cannot unassign themselves
            if obj.assignee_id == request.user.id:
                return False

            try:
                requester_membership = OrganizationMembership.objects.get(
                    user=request.user,
                    organization=obj.team.organization
                )

                curr_assignee_membership = OrganizationMembership.objects.get(
                    user_id=obj.assignee_id,
                    organization=obj.team.organization
                )

            except OrganizationMembership.DoesNotExist:
                return False

            requester_level = self.ASSIGNMENT_LEVELS.get(
                requester_membership.role
            )

            curr_assignee_level = self.ASSIGNMENT_LEVELS.get(
                curr_assignee_membership.role
            )

            if requester_level is None or curr_assignee_level is None:
                return False

            return requester_level > curr_assignee_level
        try:
            target_membership = OrganizationMembership.objects.get(user_id = assignee_id , organization = obj.team.organization)
            requester_membership = OrganizationMembership.objects.get(user=request.user,organization=obj.team.organization)
        except OrganizationMembership.DoesNotExist:
            return False

        requester_level = self.ASSIGNMENT_LEVELS.get(requester_membership.role)
        target_level = self.ASSIGNMENT_LEVELS.get(target_membership.role)

        if requester_level is None or target_level is None :
            return False

        if target_level >= requester_level:
            return False

        return obj.team.memberships.filter(user_id=assignee_id).exists()


class CanChangeIncidentTeam(BasePermission):
    ALLOWED_ROLES = {
        OrganizationMembership.Role.ADMIN,
        OrganizationMembership.Role.OWNER,
        OrganizationMembership.Role.SERVICE_MANAGER,
    }
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        try:
            membership = OrganizationMembership.objects.get(user = request.user , organization = obj.team.organization)
        except  OrganizationMembership.DoesNotExist:
            return False

        if membership.role not in self.ALLOWED_ROLES :
            return False

        target_team_id = request.data.get("team")

        if not target_team_id:
            return False

        return Team.objects.filter(id = target_team_id, organization = obj.team.organization).exists()

class CanCommentOnIncident(BasePermission):
    ALLOWED_ORG_ROLES = {
        OrganizationMembership.Role.ADMIN,
        OrganizationMembership.Role.OWNER,
    }
    TEAM_ROLES = {
        OrganizationMembership.Role.TEAM_MANAGER,
        OrganizationMembership.Role.SENIOR_ENGINEER,
        OrganizationMembership.Role.JUNIOR_ENGINEER,
        OrganizationMembership.Role.INTERN,
    }

    def has_permission(self, request, view):
        return True
    def has_object_permission(self, request, view, obj):
        incident = obj

        try:
            membership = OrganizationMembership.objects.get(
                user = request.user ,
                organization = incident.team.organization
                )
        except OrganizationMembership.DoesNotExist:
            return False

        if membership.role in self.ALLOWED_ORG_ROLES :
            return True

        if membership.role == OrganizationMembership.Role.SERVICE_MANAGER :
            return ServiceMembership.objects.filter(
                user = request.user,
                service = incident.team.service
            ).exists()

        if membership.role in self.TEAM_ROLES :
            return  incident.team.memberships.filter(
                user = request.user
            )

        return False


