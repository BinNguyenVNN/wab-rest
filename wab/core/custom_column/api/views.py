from django.db import transaction
from rest_framework.generics import UpdateAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin, \
    DestroyModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from wab.core.custom_column.api.serializers import CustomColumnTypeSerializer, \
    CustomColumnConfigValidationSerializer, \
    CustomColumnTypeValidatorSerializer, UpdateCustomColumnTypeSerializer, CreateCustomColumnMappingSerializer, \
    CreateCustomColumnTypeSerializer
from wab.core.custom_column.models import CustomColumnType, \
    CustomColumnConfigValidation, CustomColumnTypeValidator, CustomColumnMapping
from wab.core.db_provider.models import DBProviderConnection
from wab.core.serializers import SwaggerConvertDataSerializer
from wab.utils import token_authentication, responses, constant
from wab.utils.constant import MONGO
from wab.utils.db_manager import MongoDBManager
from wab.utils.paginations import ResultsSetPagination


class CustomColumnConfigValidationViewSet(CreateModelMixin, RetrieveModelMixin, ListModelMixin, UpdateModelMixin,
                                          DestroyModelMixin, GenericViewSet):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    serializer_class = CustomColumnConfigValidationSerializer
    queryset = CustomColumnConfigValidation.objects.all()
    pagination_class = ResultsSetPagination
    lookup_field = "id"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(creator=self.request.user)

    def create(self, request, *args, **kwargs):
        data = request.data
        data.update({'creator': request.user.id})
        data.update({'last_modified_by': request.user.id})
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return responses.ok(data=serializer.data, method=constant.POST,
                            entity_name='custom_column_config_validation')

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


class CustomColumnTypeViewSet(RetrieveModelMixin, ListModelMixin, DestroyModelMixin, GenericViewSet):
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


class CreateCustomColumnTypeView(CreateAPIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    serializer_class = CreateCustomColumnTypeSerializer

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        data = request.data
        custom_column_type_validator_list = data.get('custom_column_type_validator_list')
        del data['custom_column_type_validator_list']
        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            try:
                # Create Custom Column Type
                custom_column_type = serializer.save()
                # Create Custom_Column_Config_Type
                if custom_column_type_validator_list is not None:
                    for validation_item in custom_column_type_validator_list:
                        CustomColumnTypeValidator.objects.create(
                            custom_column_type=custom_column_type,
                            custom_column_config_validation_id=validation_item.get('custom_column_config_validation'),
                            operator=validation_item.get('operator'),
                            value=validation_item.get("value")
                        )

                serializer_config_type = self.get_serializer(custom_column_type)
                return responses.ok(data=serializer_config_type.data, method=constant.POST,
                                    entity_name='custom-column-type')
            except Exception as err:
                return responses.bad_request(data=str(err),
                                             message_code='UPDATE_CUSTOM_COLUMN_TYPE_HAS_ERROR')
        else:
            return responses.bad_request(data=None, message_code='UPDATE_CUSTOM_COLUMN_TYPE_INVALID')


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
                if custom_column_type_validator_delete_list is not None:
                    CustomColumnTypeValidator.objects.filter(id__in=custom_column_type_validator_delete_list).delete()

                # Update List Custom_Column_Config_Type_Validator
                if custom_column_type_validator_update_list is not None:
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
                        updated_validator.save()

                # Create List Custom_Column_Config_Type_Validator
                if custom_column_type_validator_create_list is not None:
                    for created_item in custom_column_type_validator_create_list:
                        custom_column_config_validation_id = created_item.get("custom_column_config_validation_id")
                        if custom_column_config_validation_id is not None:
                            custom_column_config_validation = CustomColumnConfigValidation.objects.get(
                                id=custom_column_config_validation_id)
                        else:
                            custom_column_config_validation = None

                        CustomColumnTypeValidator.objects.create(
                            custom_column_type=custom_column_type,
                            custom_column_config_validation=custom_column_config_validation,
                            value=created_item.get("value")
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
        try:
            connection = DBProviderConnection.objects.get(id=data.get('connection'))
            provider = connection.provider
            custom_column = CustomColumnType.objects.get(id=data.get('custom_column'))
            if provider.name == MONGO:
                mongo_db = MongoDBManager()
                db, cache_db = mongo_db.connection_mongo_by_provider(provider_connection=connection)
                # type in [str, int, float, datetime]
                table = data.get('table_name')
                column = data.get('real_column')
                data_type = custom_column.slug
                _ = mongo_db.update_convert_column_data_type(db=db, table=table, column=column,
                                                             data_type=data_type,
                                                             provider_connection_id=connection.id)
                return responses.ok(data=serializer.data, method=constant.POST,
                                    entity_name='custom_column_mapping')
            else:
                return responses.ok(data=None, method=constant.POST,
                                    entity_name='custom_column_mapping')
        except Exception as err:
            return responses.bad_request(data=str(err), message_code='MAPPING_ERROR')


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
            connection = DBProviderConnection.objects.get(id=data.get('connection'))
            provider = connection.provider
            custom_column = CustomColumnType.objects.get(id=data.get('custom_column'))
            if provider.name == MONGO:
                mongo_db = MongoDBManager()
                db, cache_db = mongo_db.connection_mongo_by_provider(provider_connection=connection)
                # type in [str, int, float, datetime]
                table = data.get('table_name')
                column = data.get('real_column')
                data_type = custom_column.slug
                _ = mongo_db.update_convert_column_data_type(db=db, table=table, column=column,
                                                             data_type=data_type,
                                                             provider_connection_id=connection.id)
                return responses.ok(data=serializer.data, method=constant.PUT,
                                    entity_name='custom_column_mapping')
            else:
                return responses.ok(data=None, method=constant.PUT,
                                    entity_name='custom_column_mapping')
        except Exception as err:
            responses.bad_request(data=str(err), message_code='CUSTOM_COLUMN_MAPPING_NOT_FOUND')


class ConvertData(UpdateAPIView):
    authentication_classes = []
    permission_classes = [AllowAny, ]
    serializer_class = SwaggerConvertDataSerializer
    pagination_class = ResultsSetPagination
    queryset = CustomColumnMapping.objects.all()

    def put(self, request, *args, **kwargs):
        data = request.data
        convert_field = data.get("convert_field")
        data_type = data.get("data_type")
        table = data.get("table")
        provider_connection_id = data.get("provider_connection_id")
        mongo_db = MongoDBManager()
        provider_connection = DBProviderConnection.objects.filter(id=provider_connection_id).first()
        db, cache_db = mongo_db.connection_mongo_by_provider(provider_connection=provider_connection)
        # type in [str, int, float, datetime]
        is_convert = mongo_db.update_convert_column_data_type(db=db, table=table, column=convert_field,
                                                              data_type=data_type,
                                                              provider_connection_id=provider_connection_id)

        return responses.ok(data={"is_convert": is_convert}, method="put", entity_name="test")


class CustomColumnValidatorListByCustomColumnIdView(RetrieveAPIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    serializer_class = CustomColumnTypeValidatorSerializer

    def get(self, request, *args, **kwargs):
        custom_column_type_id = kwargs.get("custom_column_type_id")
        try:
            custom_column_validators = CustomColumnTypeValidator.objects.filter(
                custom_column_type__id=custom_column_type_id)
            serializer = self.get_serializer(custom_column_validators, many=True)
            return responses.ok(data=serializer.data, method=constant.GET,
                                entity_name='custom-column-validator')
        except Exception as err:
            return responses.not_found(data=None, message_system=err,
                                       message_code='GET_CUSTOM_COLUMN_VALIDATOR_NOT_FOUND')


class CreateTableWithColumn(CreateAPIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    serializer_class = CreateCustomColumnMappingSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        connection_id = kwargs.get("connection_id")
        list_field = data.get("list_field")
        table_name = data.get("table_name")
        connection = DBProviderConnection.objects.filter(id=connection_id).first()
        if connection is None:
            return responses.bad_request(data=None, message_code="PROVIDER_CONNECTION_NOT_FOUND")

        if connection.provider.name == MONGO:
            mongo_db_manager = MongoDBManager()
            db, cache_db = mongo_db_manager.connection_mongo_by_provider(provider_connection=connection)
            collections = mongo_db_manager.get_all_collections(db=db, cache_db=cache_db)
            column_mapping = CustomColumnMapping.objects.filter(table_name=table_name,
                                                                connection_id=connection.id).exists()
            if column_mapping is False and table_name not in collections:
                mongo_db_manager.create_new_collection(db, table_name)
            else:
                return responses.bad_request(data=None, message_code="TABLE_NAME_IS_EXISTS")

            for field in list_field:
                try:
                    custom_column = CustomColumnType.objects.get(id=field.get('custom_column'))
                    CustomColumnMapping.objects.create(
                        connection_id=connection.id,
                        table_name=table_name,
                        real_column=field.get("column_name"),
                        custom_column_name=field.get("column_name"),
                        custom_column_id=custom_column.id
                    )
                except Exception as ex:
                    print(ex)
                    continue

        resp = CustomColumnMapping.objects.filter(connection_id=connection.id, table_name=table_name)
        serializer = self.get_serializer(resp, many=True)
        return responses.ok(data=serializer.data, method=constant.POST, entity_name="custom_column_mapping")
