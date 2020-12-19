import json

from bson.json_util import dumps
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from wab.core.db_provider.api.serializers import DbProviderSerializer, DBProviderConnectionSerializer
from wab.core.db_provider.models import DbProvider, DBProviderConnection
from wab.utils import responses, constant, token_authentication
from wab.utils.constant import MONGO
from wab.utils.db_manager import MongoDBManager


class DbProviderViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = DbProviderSerializer
    queryset = DbProvider.objects.all()
    lookup_field = "id"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.all()


class DBProviderConnectionViewSet(CreateModelMixin, RetrieveModelMixin, ListModelMixin, UpdateModelMixin,
                                  GenericViewSet):
    serializer_class = DBProviderConnectionSerializer
    queryset = DBProviderConnection.objects.all()
    lookup_field = "id"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.all()


class DBConnectionCreateView(CreateAPIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    permission_classes = [AllowAny, ]
    queryset = DbProvider.objects.all()
    serializer_class = DBProviderConnectionSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            provider = self.queryset.filter(id=data.get('provider')).first()
            if provider:
                result = serializer.save()
                if provider.name == MONGO:
                    mongo_db_manager = MongoDBManager()
                    db = mongo_db_manager.connection_mongo(host=result.host, port=result.port,
                                                           username=result.username, password=result.password,
                                                           database=result.database, ssl=result.ssl)
                    data = mongo_db_manager.get_all_collections(db=db)
                    return responses.ok(data=data, method=constant.POST, entity_name='db_provider_connection')
                else:
                    # TODO: implement another phase
                    pass
            else:
                return responses.bad_request(data='Provider not found', message_code='PROVIDER_NOT_FOUND')
        else:
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE, data=None)


class DBConnectionListTableView(ListAPIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    permission_classes = [AllowAny, ]
    queryset = DBProviderConnection.objects.all()

    def get(self, request, *args, **kwargs):
        connection_id = kwargs.get('pk', None)
        try:
            if connection_id:
                provider_connection = self.queryset.get(id=connection_id)
                provider = provider_connection.provider
                if provider:
                    if provider.name == MONGO:
                        mongo_db_manager = MongoDBManager()
                        db = mongo_db_manager.connection_mongo_by_provider(provider_connection=provider_connection)
                        data = mongo_db_manager.get_all_collections(db=db)
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
    permission_classes = [AllowAny, ]
    queryset = DBProviderConnection.objects.all()

    def get(self, request, *args, **kwargs):
        table_name = kwargs.get('table', None)
        connection_id = kwargs.get('pk', None)
        try:
            provider_connection = self.queryset.get(id=connection_id)
            provider = provider_connection.provider
            if provider:
                if provider.name == MONGO:
                    mongo_db_manager = MongoDBManager()
                    db = mongo_db_manager.connection_mongo_by_provider(provider_connection=provider_connection)
                    columns = mongo_db_manager.get_all_keys(db=db, collection=table_name)
                    return responses.ok(data=columns, method=constant.POST, entity_name='db_provider_connection')
                else:
                    # TODO: implement another phase
                    pass
            else:
                return responses.bad_request(data='Provider not found', message_code='PROVIDER_NOT_FOUND')
        except Exception as err:
            return responses.not_found(data=None, message_code='PROVIDER_CONNECTION_NOT_FOUND', message_system=err)


class DBConnectionListDataView(ListAPIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    permission_classes = [AllowAny, ]
    queryset = DBProviderConnection.objects.all()

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
                        db = mongo_db_manager.connection_mongo_by_provider(provider_connection=provider_connection)
                        documents, count = mongo_db_manager.get_all_documents(db=db, collection=table_name,
                                                                              column_sort=column_sort,
                                                                              sort=sort, page=page, page_size=page_size)
                        data = list(documents)
                        result = json.loads(dumps(data))
                        return responses.paging_data(data=result, total_count=count, method=constant.POST,
                                                     entity_name='db_provider_connection')
                    except Exception as err:
                        return responses.bad_request(data=err, message_code='BD_ERROR')
                else:
                    # TODO: implement another phase
                    pass
            else:
                return responses.bad_request(data='Provider not found', message_code='PROVIDER_NOT_FOUND')
        except DBProviderConnection.DoesNotExist as err:
            return responses.not_found(data=None, message_code='PROVIDER_CONNECTION_NOT_FOUND', message_system=err)
