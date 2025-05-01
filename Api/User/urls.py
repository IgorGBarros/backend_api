from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.conf import settings

from .views import (
    CustomTokenObtainPairView,
    FirebaseLoginView,
    CustomUserCreateView,
)   


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
router = DefaultRouter()
urlpatterns = [
    path('', include(router.urls)),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('firebase-login/', FirebaseLoginView.as_view(), name='firebase-login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/', CustomUserCreateView.as_view(), name='create-user'),
]
