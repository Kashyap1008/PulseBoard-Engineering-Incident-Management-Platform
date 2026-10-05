from django.urls import path
from .views import IncidentListCreateView,IncidentDetailView,IncidentTransitionView,IncidentAssignmentView,IncidentTeamView,IncidentSeverityView,IncidentTimelineView,IncidentCommentCreateView

urlpatterns = [
    path("",IncidentListCreateView.as_view(),name='incident-list-create'),
    path("<int:pk>/",IncidentDetailView.as_view(),name='incident-detail'),
    path("<int:pk>/transition/",IncidentTransitionView.as_view(),name='incident-transition'),
    path("<int:pk>/assign/",IncidentAssignmentView.as_view(),name='incident-assign'),
    path("<int:pk>/team/",IncidentTeamView.as_view(),name='incident-team'),
    path("<int:pk>/severity/",IncidentSeverityView.as_view(),name='incident-severity'),
    path("<int:pk>/timeline/",IncidentTimelineView.as_view(),name='incident-timeline'),
    path("<int:pk>/comments/",IncidentCommentCreateView.as_view(),name='incident-comment-create'),
]