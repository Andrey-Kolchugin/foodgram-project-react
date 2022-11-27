from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import RecipesViewSet, TagViewSet, FavoriteViewSet, IngredientsViewSet
from djoser.serializers import SetPasswordSerializer
from rest_framework_simplejwt import views


v1_router = DefaultRouter()

v1_router.register('recipes', RecipesViewSet, basename='recipes')
v1_router.register('ingredients', IngredientsViewSet, basename='ingredients')
v1_router.register('tags', TagViewSet, basename='tags')
v1_router.register(
    r'recipes/(?P<recipes_id>\d+)/favorite',
    FavoriteViewSet,
    basename='favorite'
)

urlpatterns = [
    path('', include(v1_router.urls)),
]
