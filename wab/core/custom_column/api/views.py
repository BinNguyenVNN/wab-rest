from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from wab.core.custom_column.api.serializers import CustomColumnTypeSerializer, ValidationTypeSerializer, \
    ValidationRegexSerializer, ListColumnValidationSerializer, ColumnValidationSerializer
from wab.core.custom_column.models import CustomColumnType, ValidationType, ValidationRegex, ColumnValidation


class CustomColumnTypeViewSet(CreateModelMixin, RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = CustomColumnTypeSerializer
    queryset = CustomColumnType.objects.all()
    lookup_field = "id"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.all()


class ValidationTypeViewSet(CreateModelMixin, RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
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
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    serializer_class = ListColumnValidationSerializer

    def get(self, request, *args, **kwargs):
        custom_column_id = kwargs.get('custom_column_type_id', None)
        if custom_column_id:
            validations = ColumnValidation.objects.filter(custom_column_type=custom_column_id)
            serializer = ListColumnValidationSerializer(validations, many=True)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND, data=None)


class ColumnValidationCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    serializer_class = ColumnValidationSerializer

    def post(self, request, *args, **kwargs):
        custom_column_id = kwargs.get('custom_column_type_id', None)
        if custom_column_id:
            data = request.data
            data['custom_column_type'] = custom_column_id
            serializer = ColumnValidationSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(status=status.HTTP_200_OK, data=serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND, data=None)


class ColumnValidationUpdateView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    serializer_class = ColumnValidationSerializer

    def put(self, request, *args, **kwargs):
        custom_column_id = kwargs.get('custom_column_type_id', None)
        if custom_column_id:
            data = request.data
            data['custom_column_type'] = custom_column_id
            serializer = ColumnValidationSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(status=status.HTTP_200_OK, data=serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND, data=None)
