import csv
import datetime
from io import StringIO

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import FileUploadParser

from wab.core.db_provider.models import DBProviderConnection
from wab.core.import_database.models import ImportData
from wab.core.serializers import SwaggerSerializer
from wab.utils import responses, token_authentication
from wab.utils.constant import MONGO
from wab.utils.db_manager import MongoDBManager


class ImportCsvView(CreateAPIView):
    # authentication_classes = []
    # permission_classes = [AllowAny, ]
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    serializer_class = SwaggerSerializer
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            file_obj = request.FILES['file']
            # url_csv = upload_to_s3("import", file_obj.name, file_obj, user_id=user.id)

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
                    mongo_db_manager.create_new_collection(db, table_name)
                else:
                    headers = list(csv_data.fieldnames)
                    try:
                        columns = mongo_db_manager.get_all_keys(db=db, collection=table_name)
                        if columns:
                            for header in headers:
                                if header not in columns:
                                    return responses.bad_request(
                                        data=f"Column '{header}' is not exists in table {table_name}",
                                        message_code="Column is not exists")

                    except Exception as err:
                        return responses.bad_request(data=str(err), message_code=str(err))

                # list_insert = []
                # for row in csv_data:
                #     data = dict(row)
                #     # data["_id"] = str(ObjectId())
                #     list_insert.append(data)
                #
                # print(list_insert)

                file_full_name = file_obj.name.split(".")
                time_stamp = datetime.datetime.now().timestamp()
                file_name = f"{file_full_name[0]}_{str(int(time_stamp))}.{file_full_name[1]}"
                file_name = file_name.replace(" ", "_")
                fs = FileSystemStorage(location=f"{settings.MEDIA_ROOT}/import",
                                       base_url=f"{settings.MEDIA_ROOT}/import")
                filename = fs.save(file_name, file_obj)
                uploaded_file_url = fs.url(filename)

                static_dir = f"{settings.MEDIA_ROOT}/import/{filename}"

                import_record = ImportData.objects.create(
                    provider_connection_id=connection.id,
                    username=user.username,
                    table=table_name,
                    file_url=static_dir
                )
                # process_import_database.delay(import_id=import_record.id)
                return responses.ok(data="waiting import data", method='post', entity_name='import_database')
            return responses.bad_request(data=None, message_code="SQL_PROVIDER_NOT_FOUND")

        except Exception as err:
            return responses.not_found(data=None, message_code='SQL_FUNCTION_NOT_FOUND', message_system=err)
