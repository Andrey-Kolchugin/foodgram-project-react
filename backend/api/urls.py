from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (IngredientsViewSet, RecipesViewSet, TagViewSet,
                    UserListViewSet)

v1_router = DefaultRouter()
v1_router.register('users', UserListViewSet, basename='users')
v1_router.register('recipes', RecipesViewSet, basename='recipes')
v1_router.register('ingredients', IngredientsViewSet, basename='ingredients')
v1_router.register('tags', TagViewSet, basename='tags')

urlpatterns = [
    path('', include(v1_router.urls)),
]
