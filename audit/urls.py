from django.urls import path
from .views import AuditLogApiView

urlpatterns = [
    path("",AuditLogApiView.as_view(),name='audit')
]