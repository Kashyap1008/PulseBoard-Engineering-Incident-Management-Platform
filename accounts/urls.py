from django.urls import path
from .views import RegisterView,ProfileAPIView
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenBlacklistView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    path('logout/',TokenBlacklistView.as_view(),name='logout'),


    path('profile/',ProfileAPIView.as_view(),name='profile'),
]