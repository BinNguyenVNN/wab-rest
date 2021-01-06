import csv
from io import StringIO

from rest_framework.generics import CreateAPIView
from rest_framework.parsers import FileUploadParser

from wab.core.db_provider.models import DBProviderConnection
from wab.core.import_database.models import ImportData
from wab.core.serializers import SwaggerSerializer
from wab.utils import token_authentication, responses
from wab.utils.constant import MONGO
from wab.utils.db_manager import MongoDBManager


class ImportCsvView(CreateAPIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
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
                db, cache_db = mongo_db_manager.connection_mongo_by_provider(provider_connection=connection)
                collections = mongo_db_manager.get_all_collections(db=db, cache_db=cache_db)
                if table_name not in collections:
                    return responses.bad_request(data=None, message_code="Table name is not exists")
                # table = db[table_name]
                list_insert = []

                headers = list(csv_data.fieldnames)
                try:
                    columns = mongo_db_manager.get_all_keys(db=db, collection=table_name)
                    for header in headers:
                        if header not in columns:
                            return responses.bad_request(
                                data=f"Column '{header}' is not exists in table {table_name}",
                                message_code="Column is not exists")

                except Exception as err:
                    return responses.bad_request(data=str(err), message_code="Table name is not exists")

                for row in csv_data:
                    data = dict(row)
                    # data["_id"] = str(ObjectId())
                    list_insert.append(data)

                print(list_insert)
                # insert = table.insert_many(list_insert)
                # response_id = []
                # for ids in insert.inserted_ids:
                #     response_id.append(str(ids))

                # print(response_id)
                ImportData.objects.create(
                    provider_connection_id=connection.id,
                    username='test_user',
                    table=table_name,
                    record=list_insert
                )

                return responses.ok(data="waiting import data", method='post', entity_name='import_database')
            return responses.bad_request(data=None, message_code="SQL_PROVIDER_NOT_FOUND")

        except Exception as err:
            return responses.not_found(data=None, message_code='SQL_FUNCTION_NOT_FOUND', message_system=err)
