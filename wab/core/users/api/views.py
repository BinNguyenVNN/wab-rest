from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from wab.utils import token_authentication, responses
from wab.utils.s3 import upload_to_s3, delete_s3
from .serializers import UserSerializer
from ...serializers import SwaggerSerializer

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class UploadImage(APIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    permission_classes = [AllowAny, ]
    queryset = User.objects.all()
    serializer_class = SwaggerSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        image = data.get("image")
        url = upload_to_s3(folder='avatar', file_name=image.name, file=image)
        # delete_s3(folder='avatar', file_name=image.name)

        return responses.ok(data=url)
