from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin, \
    DestroyModelMixin
from rest_framework.viewsets import GenericViewSet

from wab.core.custom_column_fk.api.serializers import CustomColumnFKSerializer
from wab.core.custom_column_fk.models import CustomColumnFK
from wab.utils import responses, constant
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
