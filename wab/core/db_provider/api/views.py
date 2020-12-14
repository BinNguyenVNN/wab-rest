from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from wab.core.db_provider.api.serializers import DbProviderSerializer
from wab.core.db_provider.models import DbProvider


class DbProviderViewSet(CreateModelMixin, RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = DbProviderSerializer
    queryset = DbProvider.objects.all()
    lookup_field = "id"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.all()
