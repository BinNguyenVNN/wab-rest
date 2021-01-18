import base64
import json

from django.conf import settings
from rest_framework.generics import ListAPIView, RetrieveAPIView

from wab.core.db_provider.models import DBProviderConnection
from wab.core.serializers import SwaggerSerializer
from wab.utils import token_authentication, responses, constant
from wab.utils.constant import MONGO
from wab.utils.db_manager import MongoDBManager


class SharingFilesGetLinkView(RetrieveAPIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    serializer_class = SwaggerSerializer

    def get(self, request, *args, **kwargs):
        connection_id = kwargs.get("connection_id")
        table_name = kwargs.get("table_name")
        try:
            sharing_key_decode = connection_id + ";" + table_name
            sharing_key_encode = base64.b64encode(bytes(sharing_key_decode, "utf-8"))
            return responses.ok(data=settings.WAB_FE + 'admin/' + sharing_key_encode, method=constant.GET, entity_name='sharing-files')
        except Exception as err:
            return responses.not_found(data=None, message_code='SHARING_FILES_CAN_NOT_CREATE_LINK', message_system=err)


class SharingFilesGetDataView(ListAPIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    queryset = DBProviderConnection.objects.all()
    serializer_class = SwaggerSerializer

    def get(self, request, *args, **kwargs):
        sharing_key_encode = kwargs.get("sharing_key")
        try:
            sharing_key_decode_utf8 = base64.b64decode(sharing_key_encode)
            sharing_key_decode = sharing_key_decode_utf8.decode("utf-8")
            sharing_key_array = sharing_key_decode.split(";")
            if len(sharing_key_array) == 2:
                connection_id = sharing_key_array[0]
                table_name = sharing_key_array[1]

                # Get data from connection and table name
                provider_connection = self.queryset.get(id=connection_id)
                provider = provider_connection.provider
                if provider:
                    if provider.name == MONGO:
                        mongo_db_manager = MongoDBManager()
                        try:
                            db, cache_db = mongo_db_manager.connection_mongo_by_provider(provider_connection=provider_connection)
                            documents, count = mongo_db_manager.get_all_documents(db=db, collection=table_name,
                                                                                  column_sort=None,
                                                                                  sort=None, page=None,
                                                                                  page_size=None)
                            data = list(documents)
                            result = json.loads(json.dumps(data))
                            return responses.ok(data=result, method=constant.GET, entity_name='sharing_files')
                        except Exception as err:
                            return responses.bad_request(data=err, message_code='BD_ERROR')
                    else:
                        # TODO: implement another phase
                        pass
                else:
                    return responses.bad_request(data='Provider not found', message_code='PROVIDER_NOT_FOUND')
            else:
                return responses.not_found(data=None, message_code='SHARING_FILES_GET_DATA_NOT_FOUND')
        except Exception as err:
            return responses.not_found(data=None, message_code='SHARING_FILES_GET_DATA_NOT_FOUND', message_system=err)
