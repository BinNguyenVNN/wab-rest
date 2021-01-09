from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from wab.core.serializers import SwaggerSerializer
from wab.utils import responses, constant
from wab.utils.operator import OPERATOR_MONGODB, MERGE_TYPE, RELATION


class ListOperatorView(ListAPIView):
    authentication_classes = []
    permission_classes = [AllowAny, ]
    serializer_class = SwaggerSerializer

    def get(self, request, *args, **kwargs):
        list_operator_mongodb = []
        for x in OPERATOR_MONGODB:
            list_operator_mongodb.append({"code": x.value[0], "name": x.value[1]})

        return responses.ok(data=list_operator_mongodb, method=constant.GET, entity_name='list-operator')


class ListJoinView(ListAPIView):
    authentication_classes = []
    permission_classes = [AllowAny, ]
    serializer_class = SwaggerSerializer

    def get(self, request, *args, **kwargs):
        list_join = []
        for x in MERGE_TYPE:
            list_join.append({"code": x.value[0], "name": x.value[1]})

        return responses.ok(data=list_join, method=constant.GET, entity_name='list_join')


class ListRelationView(ListAPIView):
    authentication_classes = []
    permission_classes = [AllowAny, ]
    serializer_class = SwaggerSerializer

    def get(self, request, *args, **kwargs):
        list_relation = []
        for x in RELATION:
            list_relation.append({"code": x.value[0], "name": x.value[1]})

        return responses.ok(data=list_relation, method=constant.GET, entity_name='list_relation')
