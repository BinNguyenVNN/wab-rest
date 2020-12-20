from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from wab.core.custom_column.api.serializers import CustomColumnTypeSerializer, ValidationTypeSerializer, \
    ValidationRegexSerializer, ListColumnValidationSerializer, ColumnValidationSerializer
from wab.core.custom_column.models import CustomColumnType, ValidationType, ValidationRegex, ColumnValidation
from wab.utils import token_authentication, responses, constant


class CustomColumnTypeViewSet(CreateModelMixin, RetrieveModelMixin, ListModelMixin,
                              UpdateModelMixin, GenericViewSet):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    serializer_class = CustomColumnTypeSerializer
    queryset = CustomColumnType.objects.all()
    lookup_field = "id"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.all()


class ValidationTypeViewSet(CreateModelMixin, RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    serializer_class = ValidationTypeSerializer
    queryset = ValidationType.objects.all()
    lookup_field = "id"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.all()


class ValidationRegexViewSet(CreateModelMixin, RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = ValidationRegexSerializer
    queryset = ValidationRegex.objects.all()
    lookup_field = "id"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.all()


class ColumnValidationListView(ListAPIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    serializer_class = ListColumnValidationSerializer

    def get(self, request, *args, **kwargs):
        custom_column_id = kwargs.get('custom_column_type_id', None)
        if custom_column_id:
            validations = ColumnValidation.objects.filter(custom_column_type=custom_column_id)
            serializer = ListColumnValidationSerializer(validations, many=True)
            return responses.ok(data=serializer.data, method=constant.GET, entity_name='column_validation')
        else:
            return responses.not_found(data=None, message_code='CUSTOM_COLUMN_NOT_FOUND')


class ColumnValidationCreateView(CreateAPIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    serializer_class = ColumnValidationSerializer

    def post(self, request, *args, **kwargs):
        custom_column_id = kwargs.get('custom_column_type_id', None)
        if custom_column_id:
            data = request.data
            data['custom_column_type'] = custom_column_id
            serializer = ColumnValidationSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return responses.ok(data=serializer.data, method=constant.POST, entity_name='column_validation')
        else:
            return responses.not_found(data=None, message_code='CUSTOM_COLUMN_NOT_FOUND')


class ColumnValidationUpdateView(UpdateAPIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    serializer_class = ColumnValidationSerializer

    def put(self, request, *args, **kwargs):
        custom_column_id = kwargs.get('custom_column_type_id', None)
        if custom_column_id:
            data = request.data
            data['custom_column_type'] = custom_column_id
            serializer = ColumnValidationSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return responses.ok(data=serializer.data, method=constant.PUT, entity_name='column_validation')
        else:
            return responses.not_found(data=None, message_code='CUSTOM_COLUMN_NOT_FOUND')
