from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.generics import UpdateAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from wab.utils import token_authentication, responses, constant
from wab.utils.s3 import upload_to_s3
from .serializers import UserSerializer, UserUpdateSerializer
from ...serializers import SwaggerSerializer

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return responses.ok(data=serializer.data, method=constant.GET, entity_name='user')


class UserUpdateProfileView(UpdateAPIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()

    def put(self, request, *args, **kwargs):
        """
                    Update user profile
                    ---
                    parameters:
                        - name: name
                          description: text
                          required: False
                          type: file
                    responseMessages:
                        - code: 200
                          message: Updated
                """
        data = request.data
        image = data.get('image')
        url = upload_to_s3(folder='avatar', file_name=image.name, file=image)
        data.update({'avatar': url})
        del data['image']
        serializer = UserUpdateSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = request.user
            user.name = data.get('name')
            user.avatar = url
            user.description = data.get('description', '')
            user.save()
            return responses.ok(data=serializer.data, method=constant.PUT, entity_name='user')


