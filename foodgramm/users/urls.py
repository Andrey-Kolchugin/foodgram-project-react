from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

v1_router = DefaultRouter()

v1_router.register('users', UserViewSet, basename='users')

urlpatterns = [
    # path('users/', UserViewSet.as_view({'post': 'post'}), name="register"),
    path('auth/', include('djoser.urls')),
    path('', include(v1_router.urls)),
]
