from django.contrib.auth import get_user_model
from requests import Response
from rest_framework import filters, permissions, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer, CustomUserSerializer, CustomUserCreateSerializer
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.pagination import PageNumberPagination
from djoser.views import UserViewSet


User = get_user_model()


class UserListViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return User.objects.all()


class UserCreateViewSet(UserViewSet):
    serializer_class = CustomUserCreateSerializer
    #
    #
    # def get_queryset(self):
    #     return User.objects.all()


# class CustomLogout(APIView):
#     permission_classes = (IsAuthenticated,)
#
#     def post(self, request):
#         try:
#             refresh_token = request.data["refresh_token"]
#             token = RefreshToken(refresh_token)
#             # print(request.data)
#             # token.blacklist()
#
#             # return Response(status=status.HTTP_205_RESET_CONTENT)
#         # except Exception as e:
#         #     print('///')
#         #     return Response(status=status.HTTP_400_BAD_REQUEST)
#


# class SignUp(APIView):
#     # permission_classes = (permissions.AllowAny,)
#     def post(self, request):
#         serializer = SignUpSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
        #
        #     username = request.data.get('username')
        #     email = request.data.get('email')
        #     user = get_object_or_404(User, username=username, email=email)
        #
        #     confirmation_code = default_token_generator.make_token(user)
        #
        #     user.password = confirmation_code
        #     user.confirmation_code = confirmation_code
        # send_mail(
        #     'Код подтверждения',
        #     confirmation_code,
        #     from_email=None,
        #     recipient_list=[user.email]
        # )
        # return Response(serializer.data, status=status.HTTP_200_OK)
