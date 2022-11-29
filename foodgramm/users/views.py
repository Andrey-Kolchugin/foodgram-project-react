import http

from django.contrib.auth import get_user_model

from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

from .serializers import UserSerializer, CustomUserSerializer, CustomUserCreateSerializer, UserSubscribeSerializer
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.pagination import PageNumberPagination
from djoser.views import UserViewSet


User = get_user_model()


class UserListViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return User.objects.all()

    @action(methods=('GET',), detail=False)
    def subscriptions(self, request):
        user = self.request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        authors = user.subscribe.all()
        result_page = self.paginate_queryset(authors)
        serializer = UserSubscribeSerializer(
            result_page, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(methods=('POST', 'DELETE'), detail=True)
    def subscribe(self, request, id):
        # serializer = UserSerializer()
        user = self.request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        following = get_object_or_404(User, pk=id)
        if request.method == 'POST':

            if User.objects.filter(id=user.id, subscribe=following).exists():
                content = {
                    "errors": "Подписка на этого пользователя уже существует!"
                }
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            if user.id == following.id:
                content = {
                    "errors": "Нельзя подписываться на самого себя!"
                }
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            user.subscribe.add(following)
            return Response(status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            if not User.objects.filter(id=user.id, subscribe=following).exists():
                content = {
                    "errors": "Подписки на этого пользователя не существует!"
                }
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            user.subscribe.remove(following)
            return Response(status=status.HTTP_204_NO_CONTENT)











# class UserCreateViewSet(UserViewSet):
#     serializer_class = CustomUserCreateSerializer
#
#     #
#     #
#     # def get_queryset(self):
#     #     return User.objects.all()



class BlacklistRefreshView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        token = request.headers.get('Authorization')
        print(token)
        # token.blacklist()
        return Response(token, status=status.HTTP_204_NO_CONTENT)

    # def post(self, obj):
        # refresh_token = request.data["refresh_token"]

            # token = RefreshToken(refresh_token)
            # print(request.data)
            # token.blacklist()

            # return Response(status=status.HTTP_205_RESET_CONTENT)
        # except Exception as e:
        #     print('///')
        #     return Response(status=status.HTTP_400_BAD_REQUEST)
        # return Response(status=status.HTTP_200_OK)
