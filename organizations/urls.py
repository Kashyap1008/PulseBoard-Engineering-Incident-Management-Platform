from django.urls import path
from .views import OrganizationListCreateView,TeamListCreateView

urlpatterns = [
    path('', OrganizationListCreateView.as_view(), name='organization-list-create'),
    path('teams/',TeamListCreateView.as_view(),name = 'team-list-create')
]