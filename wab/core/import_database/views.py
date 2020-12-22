from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from wab.core.db_provider.models import DBProviderConnection
from wab.core.import_database.serializers import ImportCsvSerializer
from wab.utils import token_authentication


class ImportCsvView(CreateAPIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    permission_classes = [AllowAny, ]
    queryset = DBProviderConnection.objects.all()
    serializer_class = ImportCsvSerializer

    def post(self, request, *args, **kwargs):
        pass
