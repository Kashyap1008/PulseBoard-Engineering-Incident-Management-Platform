from django.urls import path
from .views import (OrganizationListCreateView,
                    TeamListCreateView,
                    OrganizationRetriveDestroyView,
                    OrganizationMembersListCreateApiView,
                    OrganizationMemberRetrieveDestroyView
                    )
urlpatterns = [
    path('', OrganizationListCreateView.as_view(), name='organization-list-create'),
    path('<int:pk>/',OrganizationRetriveDestroyView.as_view(),name='organization-retrive-destroy'),
    path('members/',OrganizationMembersListCreateApiView().as_view(),'organization-members-list-create'),
    path('members/<int:pk>',OrganizationMembersListCreateApiView().as_view(),'organization-members-list-create'),
    path('teams/',TeamListCreateView.as_view(),name = 'team-list-create')
    
]  