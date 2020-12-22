from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin, \
    DestroyModelMixin
from rest_framework.viewsets import GenericViewSet

from wab.core.custom_column.api.serializers import CustomColumnRegexTypeSerializer, CustomColumnTypeSerializer, \
    CustomColumnConfigTypeSerializer, CustomColumnConfigValidationSerializer, CustomColumnConfigTypeValidatorSerializer
from wab.core.custom_column.models import CustomColumnRegexType, CustomColumnType, CustomColumnConfigType, \
    CustomColumnConfigValidation, CustomColumnConfigTypeValidator


class CustomColumnRegexTypeViewSet(CreateModelMixin, RetrieveModelMixin, ListModelMixin, UpdateModelMixin,
                                   DestroyModelMixin, GenericViewSet):
    serializer_class = CustomColumnRegexTypeSerializer
    queryset = CustomColumnRegexType.objects.all()
    lookup_field = "id"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.all()


class CustomColumnConfigTypeViewSet(CreateModelMixin, RetrieveModelMixin, ListModelMixin, UpdateModelMixin,
                                    DestroyModelMixin, GenericViewSet):
    serializer_class = CustomColumnConfigTypeSerializer
    queryset = CustomColumnConfigType.objects.all()
    lookup_field = "id"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.all()


class CustomColumnTypeViewSet(CreateModelMixin, RetrieveModelMixin, ListModelMixin, UpdateModelMixin,
                              DestroyModelMixin, GenericViewSet):
    serializer_class = CustomColumnTypeSerializer
    queryset = CustomColumnType.objects.all()
    lookup_field = "id"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.all()


class CustomColumnConfigValidationViewSet(CreateModelMixin, RetrieveModelMixin, ListModelMixin, UpdateModelMixin,
                                          DestroyModelMixin, GenericViewSet):
    serializer_class = CustomColumnConfigValidationSerializer
    queryset = CustomColumnConfigValidation.objects.all()
    lookup_field = "id"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.all()


class CustomColumnConfigTypeValidatorViewSet(CreateModelMixin, RetrieveModelMixin, ListModelMixin, UpdateModelMixin,
                                             DestroyModelMixin, GenericViewSet):
    serializer_class = CustomColumnConfigTypeValidatorSerializer
    queryset = CustomColumnConfigTypeValidator.objects.all()
    lookup_field = "id"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.all()
