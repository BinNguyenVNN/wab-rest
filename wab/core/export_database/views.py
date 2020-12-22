from django.db import transaction
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny

from wab.core.db_provider.models import DBProviderConnection
from wab.core.sql_function.api.serializers import SqlFunctionSerializer
from wab.core.sql_function.models import SqlFunction, SqlFunctionOrderBy, SqlFunctionMerge, SqlFunctionCondition, \
    SqlFunctionConditionItems
from wab.utils import token_authentication, responses, constant
import json
from bson.json_util import dumps
from wab.utils.constant import MONGO
from wab.utils.db_manager import MongoDBManager


class ExportPdfView(CreateAPIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    permission_classes = [AllowAny, ]
    serializer_class = SqlFunctionSerializer

    def post(self, request, *args, **kwargs):
        try:
            sql_functions = SqlFunction.objects.all()
            serializer = self.get_serializer(sql_functions, many=True)
            return responses.ok(data=serializer.data, method=constant.GET, entity_name='sql-function')
        except Exception as err:
            return responses.not_found(data=None, message_code='SQL_FUNCTION_NOT_FOUND', message_system=err)


class ExportExcelView(CreateAPIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    permission_classes = [AllowAny, ]
    serializer_class = SqlFunctionSerializer

    def post(self, request, *args, **kwargs):
        try:
            sql_functions = SqlFunction.objects.all()
            serializer = self.get_serializer(sql_functions, many=True)
            return responses.ok(data=serializer.data, method=constant.GET, entity_name='sql-function')
        except Exception as err:
            return responses.not_found(data=None, message_code='SQL_FUNCTION_NOT_FOUND', message_system=err)


class ExportTextView(CreateAPIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    permission_classes = [AllowAny, ]
    serializer_class = SqlFunctionSerializer

    def post(self, request, *args, **kwargs):
        try:
            sql_functions = SqlFunction.objects.all()
            serializer = self.get_serializer(sql_functions, many=True)
            return responses.ok(data=serializer.data, method=constant.GET, entity_name='sql-function')
        except Exception as err:
            return responses.not_found(data=None, message_code='SQL_FUNCTION_NOT_FOUND', message_system=err)
