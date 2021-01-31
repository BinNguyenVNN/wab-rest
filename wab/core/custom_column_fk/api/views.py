import json

from bson.json_util import dumps
from django.db import transaction
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView

from wab.core.custom_column_fk.api.serializers import CustomColumnFKSerializer
from wab.core.custom_column_fk.models import CustomColumnFK, CustomColumnFKFilter
from wab.core.db_provider.models import DBProviderConnection
from wab.core.serializers import SwaggerSerializer
from wab.utils import responses, constant, token_authentication
from wab.utils.constant import MONGO
from wab.utils.db_manager import MongoDBManager
from wab.utils.paginations import ResultsSetPagination


class CustomColumnFKListView(ListAPIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    pagination_class = ResultsSetPagination
    serializer_class = CustomColumnFKSerializer
    queryset = CustomColumnFK.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(connection__creator=request.user))
        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True)
        data_response = self.get_paginated_response(serializer.data)
        return responses.paging(data=data_response.data.get('results'), total_count=data_response.data.get('count'),
                                method=constant.GET, entity_name='custom-column-fk')


class CustomColumnFKView(RetrieveAPIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    queryset = CustomColumnFK.objects.all()
    serializer_class = CustomColumnFKSerializer

    def get(self, request, *args, **kwargs):
        try:
            custom_column_fk_id = kwargs.get("pk")
            custom_column_fk = self.get_queryset().get(id=custom_column_fk_id)
            serializer = self.serializer_class(custom_column_fk)
            return responses.ok(data=serializer.data, method=constant.GET, entity_name='custom-column-fk')
        except Exception as err:
            return responses.bad_request(data=str(err), message_code='CUSTOM_COLUMN_FK_NOT_FOUND')


class CustomColumnFKCreateView(CreateAPIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    serializer_class = CustomColumnFKSerializer

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        data = request.data
        connection_id = data.get("connection_id")
        name = data.get("name")
        table_name = data.get("table_name")
        custom_column_fk_filter_list = data.get("custom_column_fk_filter_list")
        serializer_custom_column_fk = self.get_serializer(data=data)
        if serializer_custom_column_fk.is_valid(raise_exception=True):
            try:
                # Create Custom_Column_FK
                custom_column_fk = CustomColumnFK.objects.create(
                    name=name,
                    table_name=table_name,
                    connection=DBProviderConnection.objects.get(id=connection_id),
                    creator=request.user,
                    last_modified_by=request.user
                )

                # Create Custom_Column_Filter
                if custom_column_fk_filter_list is not None:
                    for custom_column_filter in custom_column_fk_filter_list:
                        CustomColumnFKFilter.objects.create(
                            field_name=custom_column_filter.get('field_name'),
                            operator=custom_column_filter.get('operator'),
                            value=custom_column_filter.get('value'),
                            custom_column_fk=custom_column_fk
                        )

                serializer_custom_column_fk = self.get_serializer(custom_column_fk)
                return responses.ok(data=serializer_custom_column_fk.data, method=constant.POST,
                                    entity_name='custom-column-fk')
            except Exception as err:
                return responses.bad_request(data=str(err),
                                             message_code='CREATE_CUSTOM_COLUMN_FK_HAS_ERROR')
        else:
            return responses.bad_request(data=None, message_code='UPDATE_CUSTOM_COLUMN_FK_INVALID')


class CustomColumnFKUpdateView(UpdateAPIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    serializer_class = CustomColumnFKSerializer
    queryset = CustomColumnFK.objects.all()

    @transaction.atomic()
    def put(self, request, *args, **kwargs):
        custom_column_fk_id = kwargs.get('pk')
        data = request.data
        connection_id = data.get("connection_id")
        name = data.get("name")
        table_name = data.get("table_name")
        custom_column_fk_filter_create_list = data.get("custom_column_fk_filter_create_list")
        custom_column_fk_filter_update_list = data.get("custom_column_fk_filter_update_list")
        custom_column_fk_filter_delete_list = data.get("custom_column_fk_filter_delete_list")
        serializer_custom_column_fk = self.get_serializer(data=data)
        if serializer_custom_column_fk.is_valid(raise_exception=True):
            try:
                # Update Custom_Column_FK
                custom_column_fk = self.get_queryset().get(id=custom_column_fk_id)
                custom_column_fk.name = name
                custom_column_fk.table_name = table_name
                custom_column_fk.connection = DBProviderConnection.objects.get(id=connection_id)
                custom_column_fk.save()

                serializer_custom_column_fk = self.get_serializer(custom_column_fk)

                # Delete custom_column_fk_filter_list
                if custom_column_fk_filter_delete_list is not None:
                    CustomColumnFKFilter.objects.get(id__in=custom_column_fk_filter_delete_list).delete()

                # Update custom_column_fk_filter_list
                if custom_column_fk_filter_update_list is not None:
                    for item in custom_column_fk_filter_update_list:
                        custom_column_fk_filter = CustomColumnFKFilter.objects.get(
                            id=item.get('id'))
                        custom_column_fk_filter.field_name = item.get('field_name')
                        custom_column_fk_filter.operator = item.get('operator')
                        custom_column_fk_filter.value = item.get('value')
                        custom_column_fk_filter.save()

                # Create Custom_Column_Filter
                if custom_column_fk_filter_create_list is not None:
                    for custom_column_filter in custom_column_fk_filter_create_list:
                        CustomColumnFKFilter.objects.create(
                            field_name=custom_column_filter.get('field_name'),
                            operator=custom_column_filter.get('operator'),
                            value=custom_column_filter.get('value'),
                            custom_column_fk=custom_column_fk
                        )

                return responses.ok(data=serializer_custom_column_fk.data, method=constant.PUT,
                                    entity_name='custom_column_fk')
            except Exception as err:
                return responses.bad_request(data=str(err), message_code='UPDATE_CUSTOM_COLUMN_FK_HAS_ERROR')
        else:
            return responses.bad_request(data=None, message_code='UPDATE_CUSTOM_COLUMN_FK_INVALID')


class CustomColumnFKDeleteView(DestroyAPIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    serializer_class = SwaggerSerializer
    queryset = CustomColumnFK.objects.all()

    @transaction.atomic()
    def delete(self, request, *args, **kwargs):
        custom_column_fk_id = kwargs.get('pk')
        try:
            custom_column_fk = self.get_queryset().get(id=custom_column_fk_id)

            # Delete CustomColumnFKFilter
            CustomColumnFKFilter.objects.filter(custom_column_fk__id=custom_column_fk_id).delete()

            # Delete SqlFunction
            custom_column_fk.delete()

            return responses.ok(data=None, method=constant.DELETE, entity_name='custom_column_fk')
        except Exception as err:
            return responses.bad_request(data=str(err), message_code='DELETE_CUSTOM_COLUMN_FK_HAS_ERROR')


class PreviewCustomColumnFKView(ListAPIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    serializer_class = SwaggerSerializer
    pagination_class = ResultsSetPagination
    queryset = CustomColumnFK.objects.all()

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 20)
        try:
            custom_column_fk = self.get_queryset().get(id=pk)
            custom_column_filter = CustomColumnFKFilter.objects.filter(custom_column_fk=custom_column_fk)
            provider_connection = custom_column_fk.connection
            provider = provider_connection.provider
            if provider.name == MONGO:
                mongo_db_manager = MongoDBManager()
                db, cache_db = mongo_db_manager.connection_mongo_by_provider(
                    provider_connection=provider_connection)
                documents, count = mongo_db_manager.find_by_fk(db, custom_column_fk.table_name,
                                                               custom_column_filter,
                                                               page=page, page_size=page_size)

                data = list(documents)
                result = json.loads(dumps(data))
                return responses.paging_data(data=result, total_count=count, method=constant.POST,
                                             entity_name='custom_column_fk')
            else:
                return responses.paging_data(data=None, total_count=0, method=constant.POST,
                                             entity_name='custom_column_fk')
        except Exception as err:
            return responses.bad_request(data=str(err), message_code='CUSTOM_COLUMN_FK_NOT_FOUND')
