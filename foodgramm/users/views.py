from django.contrib.auth import get_user_model
from requests import Response
from rest_framework import filters, permissions, status, viewsets
from rest_framework.views import APIView

from .serializers import UserSerializer, SignUpSerializer
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.pagination import PageNumberPagination


User = get_user_model()


class UserViewSet(ListModelMixin, RetrieveModelMixin, CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination




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
