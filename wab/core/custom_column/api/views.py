from django.db import transaction
from rest_framework.generics import UpdateAPIView, CreateAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin, \
    DestroyModelMixin
from rest_framework.viewsets import GenericViewSet

from wab.core.custom_column.api.serializers import CustomColumnRegexTypeSerializer, CustomColumnTypeSerializer, \
    CustomColumnConfigValidationSerializer, \
    CustomColumnTypeValidatorSerializer, UpdateCustomColumnTypeSerializer, CreateCustomColumnMappingSerializer
from wab.core.custom_column.models import CustomColumnRegexType, CustomColumnType, \
    CustomColumnConfigValidation, CustomColumnTypeValidator, CustomColumnMapping
from wab.utils import token_authentication, responses, constant
from wab.utils.paginations import ResultsSetPagination


class CustomColumnRegexTypeViewSet(CreateModelMixin, RetrieveModelMixin, ListModelMixin, UpdateModelMixin,
                                   DestroyModelMixin, GenericViewSet):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    serializer_class = CustomColumnRegexTypeSerializer
    queryset = CustomColumnRegexType.objects.all()
    pagination_class = ResultsSetPagination
    lookup_field = "id"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True)
        data_response = self.get_paginated_response(serializer.data)
        return responses.paging(data=data_response.data.get('results'), total_count=data_response.data.get('count'),
                                method=constant.GET, entity_name='custom_column_regex_type')

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return responses.ok(data=None, method=constant.DELETE, entity_name='custom_column_regex_type')


class CustomColumnTypeViewSet(CreateModelMixin, RetrieveModelMixin, ListModelMixin, UpdateModelMixin,
                              DestroyModelMixin, GenericViewSet):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    serializer_class = CustomColumnTypeSerializer
    queryset = CustomColumnType.objects.all()
    pagination_class = ResultsSetPagination
    lookup_field = "id"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(connection__creator=request.user))
        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True)
        data_response = self.get_paginated_response(serializer.data)
        return responses.paging(data=data_response.data.get('results'), total_count=data_response.data.get('count'),
                                method=constant.GET, entity_name='custom_column_type')

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return responses.ok(data=None, method=constant.DELETE, entity_name='custom_column_type')


class CustomColumnConfigValidationViewSet(CreateModelMixin, RetrieveModelMixin, ListModelMixin, UpdateModelMixin,
                                          DestroyModelMixin, GenericViewSet):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    serializer_class = CustomColumnConfigValidationSerializer
    queryset = CustomColumnConfigValidation.objects.all()
    pagination_class = ResultsSetPagination
    lookup_field = "id"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True)
        data_response = self.get_paginated_response(serializer.data)
        return responses.paging(data=data_response.data.get('results'), total_count=data_response.data.get('count'),
                                method=constant.GET, entity_name='custom_column_config_validation')

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return responses.ok(data=None, method=constant.DELETE, entity_name='custom_column_config_validation')


class CustomColumnTypeValidatorViewSet(CreateModelMixin, RetrieveModelMixin, ListModelMixin, UpdateModelMixin,
                                       DestroyModelMixin, GenericViewSet):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    serializer_class = CustomColumnTypeValidatorSerializer
    queryset = CustomColumnTypeValidator.objects.all()
    pagination_class = ResultsSetPagination
    lookup_field = "id"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True)
        data_response = self.get_paginated_response(serializer.data)
        return responses.paging(data=data_response.data.get('results'), total_count=data_response.data.get('count'),
                                method=constant.GET, entity_name='custom_column_config_type_validator')

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return responses.ok(data=None, method=constant.DELETE, entity_name='custom_column_config_type_validator')


class UpdateCustomColumnTypeView(UpdateAPIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    serializer_class = UpdateCustomColumnTypeSerializer

    @transaction.atomic()
    def put(self, request, *args, **kwargs):
        data = request.data
        custom_column_type_id = kwargs.get("custom_column_type_id")
        name = data.get("name")
        custom_column_type_validator_delete_list = data.get("custom_column_type_validator_delete_list")
        custom_column_type_validator_update_list = data.get("custom_column_type_validator_update_list")
        custom_column_type_validator_create_list = data.get("custom_column_type_validator_create_list")
        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            try:
                # Update Custom_Column_Config_Type
                custom_column_type = CustomColumnType.objects.get(id=custom_column_type_id)
                custom_column_type.name = name
                custom_column_type.save()

                # Delete List Custom_Column_Config_Type_Validator
                for deleted_item in custom_column_type_validator_delete_list:
                    deleted_validator = CustomColumnTypeValidator.objects.get(id=deleted_item)
                    deleted_validator.delete()

                # Update List Custom_Column_Config_Type_Validator
                for updated_item in custom_column_type_validator_update_list:
                    updated_validator_id = updated_item.get("custom_column_config_type_validator_id")
                    updated_validator = CustomColumnTypeValidator.objects.get(id=updated_validator_id)
                    updated_validator.custom_column_type = custom_column_type

                    custom_column_config_validation_id = updated_item.get("custom_column_config_validation_id")
                    if custom_column_config_validation_id is not None:
                        custom_column_config_validation = CustomColumnConfigValidation.objects.get(
                            id=custom_column_config_validation_id)
                        updated_validator.custom_column_config_validation = custom_column_config_validation
                    else:
                        updated_validator.custom_column_config_validation = None

                    updated_validator.value = updated_item.get("value")

                    custom_column_regex_type_id = updated_item.get("custom_column_regex_type_id")
                    if custom_column_regex_type_id is not None:
                        custom_column_regex_type = CustomColumnRegexType.objects.get(
                            id=custom_column_regex_type_id)
                        updated_validator.custom_column_regex_type = custom_column_regex_type
                    else:
                        updated_validator.custom_column_regex_type = None
                    updated_validator.save()

                # Create List Custom_Column_Config_Type_Validator
                for created_item in custom_column_type_validator_create_list:
                    custom_column_config_validation_id = created_item.get("custom_column_config_validation_id")
                    if custom_column_config_validation_id is not None:
                        custom_column_config_validation = CustomColumnConfigValidation.objects.get(
                            id=custom_column_config_validation_id)
                    else:
                        custom_column_config_validation = None

                    custom_column_regex_type_id = created_item.get("custom_column_regex_type_id")
                    if custom_column_regex_type_id is not None:
                        custom_column_regex_type = CustomColumnRegexType.objects.get(
                            id=custom_column_regex_type_id)
                    else:
                        custom_column_regex_type = None

                    CustomColumnTypeValidator.objects.create(
                        custom_column_type=custom_column_type,
                        custom_column_config_validation=custom_column_config_validation,
                        value=created_item.get("value"),
                        custom_column_regex_type=custom_column_regex_type
                    )

                serializer_config_type = self.get_serializer(custom_column_type)
                return responses.ok(data=serializer_config_type.data, method=constant.POST,
                                    entity_name='custom-column-type')
            except Exception as err:
                return responses.bad_request(data=str(err),
                                             message_code='UPDATE_CUSTOM_COLUMN_TYPE_HAS_ERROR')
        else:
            return responses.bad_request(data=None, message_code='UPDATE_CUSTOM_COLUMN_TYPE_INVALID')


class CreateCustomColumnMappingView(CreateAPIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    serializer_class = CreateCustomColumnMappingSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return responses.ok(data=serializer.data, method=constant.POST,
                            entity_name='custom_column_mapping')


class UpdateCustomColumnMappingView(UpdateAPIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    serializer_class = CreateCustomColumnMappingSerializer
    queryset = CustomColumnMapping.objects.all()

    def update(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        try:
            data = request.data
            partial = kwargs.pop('partial', False)
            instance = CustomColumnMapping.objects.get(id=pk)
            serializer = self.serializer_class(instance, data=data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return responses.ok(data=serializer.data, method=constant.PUT,
                                entity_name='custom_column_mapping')
        except Exception as err:
            responses.bad_request(data=str(err), message_code='CUSTOM_COLUMN_MAPPING_NOT_FOUND')
