from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from wab.core.serializers import SwaggerSerializer
from wab.utils import responses, constant
from wab.utils.operator import OperatorMongo, MergeType, Relation, MongoColumnType, RegexType


class ListOperatorView(ListAPIView):
    authentication_classes = []
    permission_classes = [AllowAny, ]
    serializer_class = SwaggerSerializer

    def get(self, request, *args, **kwargs):
        list_operator_mongodb = []
        for x in OperatorMongo:
            list_operator_mongodb.append({"code": x.value[0], "name": x.value[1]})

        return responses.ok(data=list_operator_mongodb, method=constant.GET, entity_name='list-operator')


class ListJoinView(ListAPIView):
    authentication_classes = []
    permission_classes = [AllowAny, ]
    serializer_class = SwaggerSerializer

    def get(self, request, *args, **kwargs):
        list_join = []
        for x in MergeType:
            list_join.append({"code": x.value[0], "name": x.value[1]})

        return responses.ok(data=list_join, method=constant.GET, entity_name='list_join')


class ListRelationView(ListAPIView):
    authentication_classes = []
    permission_classes = [AllowAny, ]
    serializer_class = SwaggerSerializer

    def get(self, request, *args, **kwargs):
        list_relation = []
        for x in Relation:
            list_relation.append({"code": x.value[0], "name": x.value[1]})

        return responses.ok(data=list_relation, method=constant.GET, entity_name='list_relation')


class ListDataTypeView(ListAPIView):
    authentication_classes = []
    permission_classes = [AllowAny, ]
    serializer_class = SwaggerSerializer

    def get(self, request, *args, **kwargs):
        list_data_type = []
        for x in MongoColumnType:
            list_data_type.append({"code": x.value[0], "name": x.value[1]})

        return responses.ok(data=list_data_type, method=constant.GET, entity_name='list_data_type')


class ListRegexTypeView(ListAPIView):
    authentication_classes = []
    permission_classes = [AllowAny, ]
    serializer_class = SwaggerSerializer

    def get(self, request, *args, **kwargs):
        list_regex_type = []
        for x in RegexType:
            list_regex_type.append({"code": x.value[0], "name": x.value[1]})

        return responses.ok(data=list_regex_type, method=constant.GET, entity_name='list_regex_type')
