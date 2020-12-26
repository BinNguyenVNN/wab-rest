from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin, \
    DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from wab.core.custom_column_fk.api.serializers import CustomColumnFKSerializer
from wab.core.custom_column_fk.models import CustomColumnFK


class CustomColumnFKViewSet(CreateModelMixin, RetrieveModelMixin, ListModelMixin, UpdateModelMixin,
                            DestroyModelMixin, GenericViewSet):
    serializer_class = CustomColumnFKSerializer
    queryset = CustomColumnFK.objects.all()
    lookup_field = "id"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.all()