import json

from bson.json_util import dumps
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin, \
    DestroyModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from wab.core.custom_column.models import CustomColumnMapping
from wab.core.db_provider.api.serializers import DbProviderSerializer, DBProviderConnectionSerializer
from wab.core.db_provider.models import DbProvider, DBProviderConnection
from wab.core.serializers import SwaggerSerializer
from wab.utils import responses, constant, token_authentication
from wab.utils.constant import MONGO
from wab.utils.db_manager import MongoDBManager
from wab.utils.paginations import ResultsSetPagination


class DbProviderViewSet(CreateModelMixin, ListModelMixin, GenericViewSet, DestroyModelMixin):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    serializer_class = DbProviderSerializer
    queryset = DbProvider.objects.all()
    lookup_field = "id"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return responses.ok(data=None, method=constant.DELETE, entity_name='db_provider')


class DBProviderConnectionViewSet(CreateModelMixin, RetrieveModelMixin, ListModelMixin, UpdateModelMixin,
                                  DestroyModelMixin, GenericViewSet):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    serializer_class = DBProviderConnectionSerializer
    pagination_class = ResultsSetPagination
    queryset = DBProviderConnection.objects.all()
    lookup_field = "id"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(creator=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True)
        data_response = self.get_paginated_response(serializer.data)
        return responses.paging(data=data_response.data.get('results'), total_count=data_response.data.get('count'),
                                method=constant.GET, entity_name='db_provider_connection')

    def create(self, request, *args, **kwargs):
        data = request.data
        data.update({'creator': request.user.id})
        data.update({'last_modified_by': request.user.id})
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        return responses.ok(data=serializer.data, method=constant.POST,
                            entity_name='db_provider_connection')

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return responses.ok(data=None, method=constant.DELETE, entity_name='db_provider_connection')


class CheckView(ListAPIView):
    authentication_classes = []
    permission_classes = []
    queryset = DBProviderConnection.objects.all()

    def get(self, request, *args, **kwargs):
        provider_connection = self.queryset.get(id=1)
        mongo_db_manager = MongoDBManager()
        db, cache_db = mongo_db_manager.connection_mongo_by_provider(
            provider_connection=provider_connection)
        result = mongo_db_manager.check_column_data_type(db, 'order_items', 'price')
        return responses.ok(data=result, method=constant.GET, entity_name='db_provider_connection')


class DBConnectionConnectView(CreateAPIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    queryset = DbProvider.objects.all()
    serializer_class = DBProviderConnectionSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        # data.update({'creator': request.user.id})
        # data.update({'last_modified_by': request.user.id})
        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            provider = self.queryset.filter(id=data.get('provider')).first()
            if provider:
                try:
                    if provider.name == MONGO:
                        mongo_db_manager = MongoDBManager()
                        db, cache_db = mongo_db_manager.connection_mongo(host=data.get('host'), port=data.get('port'),
                                                                         username=data.get('username'),
                                                                         password=data.get('password'),
                                                                         database=data.get('database'),
                                                                         ssl=data.get('ssl'), user_id=request.user.id)
                        collections = mongo_db_manager.get_all_collections(db=db, cache_db=cache_db)
                        # serializer.save()
                        return responses.ok(data=collections, method=constant.POST,
                                            entity_name='db_provider_connection')
                    else:
                        # TODO: implement another phase
                        pass
                except Exception as err:
                    return responses.bad_request(data=str(err), message_code='CONNECT_ERROR')
            else:
                return responses.bad_request(data='Provider not found', message_code='PROVIDER_NOT_FOUND')
        else:
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE, data=None)


class DBConnectionListTableView(ListAPIView):
    authentication_classes = (token_authentication.JWTAuthenticationBackend,)
    queryset = DBProviderConnection.objects.all()
    serializer_class = SwaggerSerializer

    def get(self, request, *args, **kwargs):
        connection_id = kwargs.get('pk', None)
        try:
            if connection_id:
                provider_connection = self.queryset.get(id=connection_id)
                provider = provider_connection.provider
                if provider:
                    if provider.name == MONGO:
                        mongo_db_manager = MongoDBManager()
                        db, cache_db = mongo_db_manager.connection_mongo_by_provider(
                            provider_connection=provider_connection)
                        data = mongo_db_manager.get_all_collections(db=db, cache_db=cache_db)
                        return responses.ok(data=data, method=constant.POST, entity_name='db_provider_connection')
                    else:
                        # TODO: implement another phase
                        pass
                else:
                    return responses.bad_request(data='Provider not found', message_code='PROVIDER_NOT_FOUND')
            else:
                return responses.bad_request(data=None, message_code='PROVIDER_CONNECTION_ID_EMPTY')
        except Exception as err:
            return responses.not_found(data=None, message_code='PROVIDER_CONNECTION_NOT_FOUND', message_system=err)


class DBConnectionListColumnView(ListAPIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    queryset = DBProviderConnection.objects.all()
    serializer_class = SwaggerSerializer

    def get(self, request, *args, **kwargs):
        table_name = kwargs.get('table', None)
        connection_id = kwargs.get('pk', None)
        try:
            provider_connection = self.queryset.get(id=connection_id)
            provider = provider_connection.provider
            if provider:
                if provider.name == MONGO:
                    mongo_db_manager = MongoDBManager()
                    db, cache_db = mongo_db_manager.connection_mongo_by_provider(
                        provider_connection=provider_connection)
                    # TODO: PhuongTN -> get real column from database
                    columns = []
                    real_columns = mongo_db_manager.get_all_keys(db=db, collection=table_name)
                    # TODO: PhuongTN -> get custom column mapping
                    custom_columns = CustomColumnMapping.objects.filter(connection_id=connection_id,
                                                                        table_name=table_name)
                    if custom_columns.exists():
                        custom_columns = custom_columns
                        for rc in real_columns:
                            is_append = False
                            for cc in custom_columns:
                                if rc == cc.real_column:
                                    obj = {
                                        'id': cc.id,
                                        'real_column': cc.real_column,
                                        'custom_column_name': cc.custom_column_name,
                                        'custom_column_id': cc.custom_column.id
                                    }
                                    columns.append(obj)
                                    is_append = True
                                    break
                            if not is_append:
                                obj = {
                                    'id': None,
                                    'real_column': rc,
                                    'custom_column_name': None,
                                    'custom_column_id': None
                                }
                                columns.append(obj)

                    else:
                        for rc in real_columns:
                            obj = {
                                'id': None,
                                'real_column': rc,
                                'custom_column_name': None,
                                'custom_column_id': None
                            }
                            columns.append(obj)

                    return responses.ok(data=columns, method=constant.POST, entity_name='db_provider_connection')
                else:
                    # TODO: implement another phase
                    pass
            else:
                return responses.bad_request(data='Provider not found', message_code='PROVIDER_NOT_FOUND')
        except Exception as err:
            return responses.not_found(data=None, message_code='PROVIDER_CONNECTION_NOT_FOUND', message_system=str(err))


class DBConnectionListDataView(ListAPIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    queryset = DBProviderConnection.objects.all()
    serializer_class = SwaggerSerializer
    pagination_class = ResultsSetPagination

    def get(self, request, *args, **kwargs):
        table_name = kwargs.get('table', None)
        connection_id = kwargs.get('pk', None)
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 20)
        column_sort = request.GET.get('column_sort', None)
        sort = request.GET.get('sort', None)
        try:
            provider_connection = self.queryset.get(id=connection_id)
            provider = provider_connection.provider
            if provider:
                if provider.name == MONGO:
                    mongo_db_manager = MongoDBManager()
                    try:
                        db, cache_db = mongo_db_manager.connection_mongo_by_provider(
                            provider_connection=provider_connection)
                        documents, count = mongo_db_manager.get_all_documents(db=db, collection=table_name,
                                                                              column_sort=column_sort,
                                                                              sort=sort, page=page, page_size=page_size)

                        data = list(documents)
                        result = json.loads(dumps(data))
                        return responses.paging_data(data=result, total_count=count, method=constant.POST,
                                                     entity_name='db_provider_connection')
                    except Exception as err:
                        return responses.bad_request(data=str(err), message_code='BD_ERROR')
                else:
                    # TODO: implement another phase
                    pass
            else:
                return responses.bad_request(data='Provider not found', message_code='PROVIDER_NOT_FOUND')
        except DBProviderConnection.DoesNotExist as err:
            return responses.not_found(data=None, message_code='PROVIDER_CONNECTION_NOT_FOUND', message_system=err)
