from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserListViewSet
from djoser.views import UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

v1_router = DefaultRouter()
#
v1_router.register('users', UserListViewSet, basename='users')

urlpatterns = [
    path('', include(v1_router.urls)),
    # path('', include('djoser.urls')),
]
