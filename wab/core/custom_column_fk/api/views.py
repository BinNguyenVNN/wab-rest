from rest_framework.generics import ListAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin, \
    DestroyModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from wab.core.custom_column_fk.api.serializers import CustomColumnFKSerializer
from wab.core.custom_column_fk.models import CustomColumnFK
from wab.core.serializers import SwaggerSerializer
from wab.utils import responses, constant, token_authentication
from wab.utils.operator import OPERATOR_MONGODB
from wab.utils.paginations import ResultsSetPagination


class CustomColumnFKViewSet(CreateModelMixin, RetrieveModelMixin, ListModelMixin, UpdateModelMixin,
                            DestroyModelMixin, GenericViewSet):
    serializer_class = CustomColumnFKSerializer
    queryset = CustomColumnFK.objects.all()
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
                                method=constant.GET, entity_name='custom_column_fk')

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return responses.ok(data=None, method=constant.DELETE, entity_name='custom_column_fk')


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
