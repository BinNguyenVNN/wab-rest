from django.db import transaction
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin, \
    DestroyModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from wab.core.custom_column.api.serializers import CustomColumnRegexTypeSerializer, CustomColumnTypeSerializer, \
    CustomColumnConfigTypeSerializer, CustomColumnConfigValidationSerializer, CustomColumnConfigTypeValidatorSerializer, \
    UpdateCustomColumnConfigTypeSerializer
from wab.core.custom_column.models import CustomColumnRegexType, CustomColumnType, CustomColumnConfigType, \
    CustomColumnConfigValidation, CustomColumnConfigTypeValidator
from wab.utils import token_authentication, responses, constant


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


class UpdateCustomColumnConfigTypeView(UpdateAPIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    permission_classes = [AllowAny, ]
    serializer_class = UpdateCustomColumnConfigTypeSerializer

    @transaction.atomic()
    def put(self, request, *args, **kwargs):
        data = request.data
        config_type_id = kwargs.get("config_type_id")
        name = data.get("name")
        config_type_validator_delete_list = data.get("config_type_validator_delete_list")
        config_type_validator_update_list = data.get("config_type_validator_update_list")
        config_type_validator_create_list = data.get("config_type_validator_create_list")
        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            try:
                # Update Custom_Column_Config_Type
                custom_column_config_type = CustomColumnConfigType.objects.get(id=config_type_id)
                custom_column_config_type.name = name
                custom_column_config_type.save()

                # Delete List Custom_Column_Config_Type_Validator
                for deleted_item in config_type_validator_delete_list:
                    deleted_validator = CustomColumnConfigTypeValidator.objects.get(id=deleted_item)
                    deleted_validator.delete()

                # Update List Custom_Column_Config_Type_Validator
                for updated_item in config_type_validator_update_list:
                    updated_validator = CustomColumnConfigTypeValidator.objects.get(id=updated_item)
                    updated_validator.custom_column_config_type = custom_column_config_type
                    updated_validator.custom_column_config_validation = updated_item.get(
                        "custom_column_config_validation")
                    updated_validator.value = updated_item.get("value")
                    updated_validator.custom_column_regex_type = updated_item.get("custom_column_regex_type")
                    updated_validator.save()

                # Create List Custom_Column_Config_Type_Validator
                for created_item in config_type_validator_create_list:
                    CustomColumnConfigTypeValidator.objects.create(
                        custom_column_config_type=custom_column_config_type,
                        custom_column_config_validation=created_item.get("custom_column_config_validation"),
                        value=created_item.get("value"),
                        custom_column_regex_type=created_item.get("custom_column_regex_type")
                    )

                serializer_config_type = self.get_serializer(custom_column_config_type)
                return responses.ok(data=serializer_config_type.data, method=constant.POST,
                                    entity_name='custom-column-config-type')
            except Exception as err:
                return responses.bad_request(data=None,
                                             message_code='UPDATE_CUSTOM_COLUMN_CONFIG_TYPE_HAS_ERROR',
                                             message_system=err)
        else:
            return responses.bad_request(data=None, message_code='UPDATE_CUSTOM_COLUMN_CONFIG_TYPE_INVALID')
