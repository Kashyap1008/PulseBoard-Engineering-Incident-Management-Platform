from rest_framework.permissions import BasePermission

class IsOrganizationMember(BasePermission):
    def has_permission(self, request, view):
        organization_id = request.data.get("organization")

        if request.method == 'GET':
            return True

        if not organization_id :
            return False
        
        return request.user.organization_memberships.filter(
            organization__id = organization_id
        ).exists()

