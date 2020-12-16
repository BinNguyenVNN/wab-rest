from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.response import Response
from wab.core.db_provider.api.serializers import DbProviderSerializer, DBProviderConnectionSerializer
from wab.core.db_provider.models import DbProvider, DBProviderConnection
from wab.utils.constant import MONGO
from wab.utils.db_manager import MongoDBManager


class DbProviderViewSet(CreateModelMixin, RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
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
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    serializer_class = DBProviderConnectionSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            provider = DbProvider.objects.filter(id=data.get('provider')).first()
            if provider:
                result = serializer.save()
                if provider.name == MONGO:
                    mongo_db_manager = MongoDBManager()
                    db = mongo_db_manager.connection_mongo(host=result.host, port=result.port,
                                                           username=result.username, password=result.password,
                                                           database=result.database, ssl=result.ssl)
                    data = mongo_db_manager.get_all_collections(db=db)
                else:
                    pass
                return Response(status=status.HTTP_200_OK, data=data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND, data="Provider not found")
        else:
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE, data=None)
