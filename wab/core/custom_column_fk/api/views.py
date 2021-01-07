import json

from bson.json_util import dumps
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin, \
    DestroyModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from wab.core.custom_column_fk.api.serializers import CustomColumnFKSerializer
from wab.core.custom_column_fk.models import CustomColumnFK
from wab.core.serializers import SwaggerSerializer
from wab.utils import responses, constant, token_authentication
from wab.utils.constant import MONGO
from wab.utils.db_manager import MongoDBManager
from wab.utils.operator import OPERATOR_MONGODB
from wab.utils.paginations import ResultsSetPagination


class CustomColumnFKViewSet(CreateModelMixin, RetrieveModelMixin, ListModelMixin, UpdateModelMixin,
                            DestroyModelMixin, GenericViewSet):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    serializer_class = CustomColumnFKSerializer
    queryset = CustomColumnFK.objects.all()
    pagination_class = ResultsSetPagination
    lookup_field = "id"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(creator=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True)
        data_response = self.get_paginated_response(serializer.data)
        return responses.paging(data=data_response.data.get('results'), total_count=data_response.data.get('count'),
                                method=constant.GET, entity_name='custom_column_fk')

    def create(self, request, *args, **kwargs):
        data = request.data
        data.update({'creator': request.user.id})
        data.update({'last_modified_by': request.user.id})
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return responses.ok(data=serializer.data, method=constant.POST,
                            entity_name='custom_column_fk')

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return responses.ok(data=None, method=constant.DELETE, entity_name='custom_column_fk')


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
            provider_connection = custom_column_fk.connection
            provider = provider_connection.provider
            if provider.name == MONGO:
                mongo_db_manager = MongoDBManager()
                db, cache_db = mongo_db_manager.connection_mongo_by_provider(
                    provider_connection=provider_connection)
                documents, count = mongo_db_manager.find_by_fk(db, custom_column_fk.table_name,
                                                               custom_column_fk.field_name,
                                                               custom_column_fk.operator, custom_column_fk.value,
                                                               page=page, page_size=page_size)

                data = list(documents)
                result = json.loads(dumps(data))
                return responses.paging_data(data=result, total_count=count, method=constant.POST,
                                             entity_name='custom_column_fk')
            else:
                pass
        except Exception as err:
            return responses.bad_request(data=str(err), message_code='CUSTOM_COLUMN_FK_NOT_FOUND')


class ListOperatorMongoDBView(ListAPIView):
    authentication_classes = []
    permission_classes = [AllowAny, ]
    queryset = CustomColumnFK.objects.all()
    serializer_class = SwaggerSerializer

    def get(self, request, *args, **kwargs):
        list_operator_mongodb = []
        for x in OPERATOR_MONGODB:
            list_operator_mongodb.append({"code": x.value[0], "name": x.value[1]})

        return responses.ok(data=list_operator_mongodb, method=constant.GET, entity_name='custom_column_fk')
