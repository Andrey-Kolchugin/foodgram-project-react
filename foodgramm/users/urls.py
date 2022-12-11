from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserListViewSet
from djoser.views import UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

v1_router = DefaultRouter()
v1_router.register('', UserListViewSet, basename='users')

urlpatterns = [
    path('set_password/', UserViewSet.as_view({"post": "set_password"}), name="set_password"),
    # path('auth/token/login/', include('djoser.urls.authtoken')),
    # path('token/login/', TokenObtainPairView.as_view(), name="login"),
    path('', include(v1_router.urls)),
]
