import io
from datetime import datetime
import xlsxwriter as xlsxwriter
from django.http import HttpResponse
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from wab.core.db_provider.models import DBProviderConnection
from wab.core.serializers import SwaggerSerializer
from wab.utils import token_authentication, responses
import json
from bson.json_util import dumps
from wab.utils.constant import MONGO
from wab.utils.db_manager import MongoDBManager
from wab.utils.export_manager import GeneratePdf


class ExportPdfView(ListAPIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    permission_classes = [AllowAny, ]
    queryset = DBProviderConnection.objects.all()
    serializer_class = SwaggerSerializer

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
    serializer_class = SwaggerSerializer

    def get(self, request, *args, **kwargs):
        try:
            connection_id = kwargs.get("connection")
            table_name = kwargs.get("table_name")
            connection = DBProviderConnection.objects.filter(id=connection_id).first()
            if connection.provider.name == MONGO:
                mongo_db_manager = MongoDBManager()
                db = mongo_db_manager.connection_mongo_by_provider(provider_connection=connection)
                c = db.__getattr__(table_name).find().limit(20)

                result = json.loads(dumps(list(c)))
                headers = list(result[0].keys())

                output = io.BytesIO()
                workbook = xlsxwriter.Workbook(output)
                worksheet = workbook.add_worksheet()

                cell_format_header = workbook.add_format()
                cell_format_header.set_bold()

                for index in range(len(headers)):
                    worksheet.write(0, index, headers[index], cell_format_header)

                for row_num, columns in enumerate(result):
                    for index in range(len(headers)):
                        value = columns.get(headers[index]) if index != 0 else columns.get(headers[index]).get('$oid')
                        worksheet.write(row_num + 1, index, value)

                workbook.close()

                output.seek(0)

                today = datetime.now().strftime("%d/%m/%Y_%H%M%S")
                filename = f"ExportData-{table_name}-{today}.xlsx"
                response = HttpResponse(
                    output,
                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
                response['Content-Disposition'] = 'attachment; filename=%s' % filename

                return response
            return responses.bad_request(data=None, message_code="SQL_PROVIDER_NOT_FOUND")
        except Exception as err:
            return responses.not_found(data=None, message_code='SQL_FUNCTION_NOT_FOUND', message_system=err)


class ExportTextView(ListAPIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    permission_classes = [AllowAny, ]
    serializer_class = SwaggerSerializer

    def get(self, request, *args, **kwargs):
        try:
            connection_id = kwargs.get("connection")
            table_name = kwargs.get("table_name")
            connection = DBProviderConnection.objects.filter(id=connection_id).first()
            if connection.provider.name == MONGO:
                mongo_db_manager = MongoDBManager()
                db = mongo_db_manager.connection_mongo_by_provider(provider_connection=connection)
                c = db.__getattr__(table_name).find().limit(20)

                result = json.loads(dumps(list(c)))
                headers = list(result[0].keys())

                content = ''
                for header in headers:
                    content += header
                    if headers.index(header) != len(headers) - 1:
                        content += ', '
                    else:
                        content += '\n'

                for value in result:
                    for header in headers:
                        if header == "_id":
                            content += value.get(header).get('$oid')
                        else:
                            content += value.get(header)
                        if headers.index(header) != len(headers) - 1:
                            content += ', '
                        else:
                            content += '\n'

                today = datetime.now().strftime("%d/%m/%Y_%H%M%S")
                filename = f"ExportData-{table_name}-{today}.txt"
                response = HttpResponse(content, content_type='text/plain')
                response['Content-Disposition'] = 'attachment; filename=%s' % filename

                return response
            return responses.bad_request(data=None, message_code="SQL_PROVIDER_NOT_FOUND")
        except Exception as err:
            return responses.not_found(data=None, message_code='SQL_FUNCTION_NOT_FOUND', message_system=err)
