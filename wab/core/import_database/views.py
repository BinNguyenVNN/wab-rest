import csv
import json

from bson import ObjectId
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import AllowAny

from wab.core.db_provider.models import DBProviderConnection
from wab.core.import_database.serializers import ImportCsvSerializer
from wab.core.serializers import SwaggerSerializer
from wab.utils import token_authentication, responses
from io import StringIO

from wab.utils.constant import MONGO
from wab.utils.db_manager import MongoDBManager
from bson.json_util import dumps


class ImportCsvView(CreateAPIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    permission_classes = [AllowAny, ]
    serializer_class = SwaggerSerializer
    parser_class = (FileUploadParser,)

    def post(self, request, **kwargs):
        try:
            file_obj = request.FILES['file']

            file = file_obj.read().decode('utf-8')
            csv_data = csv.DictReader(StringIO(file))

            connection_id = kwargs.get("connection")
            table_name = kwargs.get("table_name")
            connection = DBProviderConnection.objects.filter(id=connection_id).first()
            if connection.provider.name == MONGO:
                mongo_db_manager = MongoDBManager()
                db = mongo_db_manager.connection_mongo_by_provider(provider_connection=connection)
                table = db[table_name]
                list_insert = []

                for row in csv_data:
                    data = dict(row)
                    data["_id"] = ObjectId()
                    list_insert.append(data)

                print(list_insert)
                insert = table.insert_many(list_insert)
                response_id = []
                for ids in insert.inserted_ids:
                    response_id.append(str(ids))

                print(response_id)

                return responses.ok(data=response_id, method='post', entity_name='import_database')
            return responses.bad_request(data=None, message_code="SQL_PROVIDER_NOT_FOUND")

        except Exception as err:
            return responses.not_found(data=None, message_code='SQL_FUNCTION_NOT_FOUND', message_system=err)
