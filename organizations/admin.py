from django.contrib import admin

# Register your models here.
from .models import Organization,OrganizationMembership,Team,TeamMembership,Service,ServiceMembership

admin.site.register(Organization)
admin.site.register(Service)
admin.site.register(Team)
admin.site.register(TeamMembership)
admin.site.register(OrganizationMembership)
admin.site.register(ServiceMembership)
