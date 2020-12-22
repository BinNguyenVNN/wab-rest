from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from wab.core.db_provider.models import DBProviderConnection
from wab.core.sql_function.api.serializers import SqlFunctionSerializer
from wab.core.sql_function.models import SqlFunction
from wab.utils import token_authentication, responses, constant
import json
from bson.json_util import dumps
from wab.utils.constant import MONGO
from wab.utils.db_manager import MongoDBManager
from wab.utils.export_manager import GeneratePdf


class ExportPdfView(ListAPIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    queryset = DBProviderConnection.objects.all()

    def get(self, request, *args, **kwargs):
        start = request.GET.get('start', None)
        end = request.GET.get('end', None)
        table_name = kwargs.get('table_name', None)
        connection_id = kwargs.get('connection', None)
        provider_connection = self.queryset.get(id=connection_id)
        provider = provider_connection.provider
        try:
            if provider:
                if provider.name == MONGO:
                    mongo_db_manager = MongoDBManager()
                    try:
                        db = mongo_db_manager.connection_mongo_by_provider(provider_connection=provider_connection)
                        columns = mongo_db_manager.get_all_keys(db=db, collection=table_name)
                        documents, count = mongo_db_manager.get_all_documents(db=db, collection=table_name,
                                                                              column_sort=None,
                                                                              sort=None, page=1, page_size=20)
                        data = list(documents)
                        result = json.loads(dumps(data))
                        # final_data = []
                        # for d in result:
                        #     i = []
                        #     for k,v in d.items():
                        #         i.append(v)
                        #     final_data.append(i)
                        pdf = GeneratePdf(result, table_name, columns)
                        response = pdf.generate_pdf(context={})
                        return response
                    except Exception as err:
                        return responses.bad_request(data=err, message_code='BD_ERROR')
                else:
                    # TODO: implement another phase
                    pass
            else:
                return responses.bad_request(data='Provider not found', message_code='PROVIDER_NOT_FOUND')
        except DBProviderConnection.DoesNotExist as err:
            return responses.not_found(data=None, message_code='EXPORT_ERROR', message_system=err)


class ExportExcelView(ListAPIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    permission_classes = [AllowAny, ]
    serializer_class = SqlFunctionSerializer

    def get(self, request, *args, **kwargs):
        try:
            sql_functions = SqlFunction.objects.all()
            serializer = self.get_serializer(sql_functions, many=True)
            return responses.ok(data=serializer.data, method=constant.GET, entity_name='sql-function')
        except Exception as err:
            return responses.not_found(data=None, message_code='SQL_FUNCTION_NOT_FOUND', message_system=err)


class ExportTextView(ListAPIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    permission_classes = [AllowAny, ]
    serializer_class = SqlFunctionSerializer

    def get(self, request, *args, **kwargs):
        try:
            sql_functions = SqlFunction.objects.all()
            serializer = self.get_serializer(sql_functions, many=True)
            return responses.ok(data=serializer.data, method=constant.GET, entity_name='sql-function')
        except Exception as err:
            return responses.not_found(data=None, message_code='SQL_FUNCTION_NOT_FOUND', message_system=err)
