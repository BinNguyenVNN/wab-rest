import json

from bson.json_util import dumps
from django.db import transaction
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny

from wab.core.db_provider.models import DBProviderConnection
from wab.core.serializers import SwaggerSerializer
from wab.core.sql_function.api.serializers import SqlFunctionSerializer
from wab.core.sql_function.models import SqlFunction, SqlFunctionOrderBy, SqlFunctionMerge, SqlFunctionConditionItems
from wab.utils import token_authentication, responses, constant
from wab.utils.constant import MONGO
from wab.utils.db_manager import MongoDBManager
from wab.utils.paginations import ResultsSetPagination


class SqlFunctionListView(ListAPIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    pagination_class = ResultsSetPagination
    serializer_class = SqlFunctionSerializer
    queryset = SqlFunction.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(connection__creator=request.user))
        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True)
        data_response = self.get_paginated_response(serializer.data)
        return responses.paging(data=data_response.data.get('results'), total_count=data_response.data.get('count'),
                                method=constant.GET, entity_name='sql-function')


class SqlFunctionCreateView(CreateAPIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    serializer_class = SqlFunctionSerializer

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        data = request.data
        name = data.get('name')
        connection = data.get('connection')
        order_by_name = data.get('order_by_name')
        sql_function_merges = data.get('sql_function_merges')
        sql_function_condition_items = data.get('sql_function_condition_items')
        serializer_sql_function = self.get_serializer(data=data)
        if serializer_sql_function.is_valid(raise_exception=True):
            try:
                # Create SqlFunction
                sql_function = SqlFunction.objects.create(
                    name=name,
                    connection=DBProviderConnection.objects.get(id=connection)
                )
                serializer_sql_function = self.get_serializer(sql_function)
                # Create SqlFunctionOrderBy
                SqlFunctionOrderBy.objects.create(
                    order_by_name=order_by_name,
                    sql_function=sql_function
                )
                # Create SqlFunctionMerge
                for sql_function_merge in sql_function_merges:
                    SqlFunctionMerge.objects.create(
                        table_name=sql_function_merge.get('table_name'),
                        column_name=sql_function_merge.get('column_name'),
                        merge_type=sql_function_merge.get('merge_type'),
                        sql_function=sql_function
                    )

                # # Create SqlFunctionCondition
                # sql_function_condition = SqlFunctionCondition.objects.create(
                #     sql_function=sql_function
                # )

                # Create SqlFunctionConditionItems
                for sql_function_condition_item in sql_function_condition_items:
                    SqlFunctionConditionItems.objects.create(
                        table_name=sql_function_condition_item.get('table_name'),
                        field_name=sql_function_condition_item.get('field_name'),
                        sql_function=sql_function,
                        value=sql_function_condition_item.get('value'),
                        operator=sql_function_condition_item.get('operator'),
                        relation=sql_function_condition_item.get('relation')
                    )

                return responses.ok(data=serializer_sql_function.data, method=constant.POST, entity_name='sql-function')
            except Exception as err:
                return responses.bad_request(data=str(err),
                                             message_code='CREATE_SQL_FUNCTION_HAS_ERROR')
        else:
            return responses.bad_request(data=None, message_code='CREATE_SQL_FUNCTION_INVALID')


class SqlFunctionUpdateView(UpdateAPIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    serializer_class = SqlFunctionSerializer
    queryset = SqlFunction.objects.all()

    @transaction.atomic()
    def put(self, request, *args, **kwargs):
        sql_function_id = kwargs.get('pk')
        data = request.data
        name = data.get('name')
        connection = data.get('connection')
        sql_function_order_by_id = data.get('sql_function_order_by_id')
        order_by_name = data.get('order_by_name')
        sql_function_merges = data.get('sql_function_merges')
        sql_function_condition_items = data.get('sql_function_condition_items')
        serializer_sql_function = self.get_serializer(data=data)
        if serializer_sql_function.is_valid(raise_exception=True):
            try:
                # Update SqlFunction
                sql_function = self.get_queryset().get(
                    id=sql_function_id
                )
                sql_function.name = name
                sql_function.connection = DBProviderConnection.objects.get(id=connection)
                sql_function.save()

                serializer_sql_function = self.get_serializer(sql_function)

                # Update SqlFunctionOrderBy
                sql_function_order_by = SqlFunctionOrderBy.objects.get(id=sql_function_order_by_id)
                sql_function_order_by.order_by_name = order_by_name
                sql_function_order_by.save()

                # Update SqlFunctionMerge
                for item in sql_function_merges:
                    sql_function_merge = SqlFunctionMerge.objects.get(id=item.get('sql_function_merge_id'))
                    sql_function_merge.table_name = item.get('table_name')
                    sql_function_merge.merge_type = item.get('merge_type')
                    sql_function_merge.column_name = item.get('column_name'),
                    sql_function_merge.save()

                # Update SqlFunctionConditionItems
                for item in sql_function_condition_items:
                    sql_function_condition_item = SqlFunctionConditionItems.objects.get(
                        id=item.get('sql_function_condition_item_id'))
                    sql_function_condition_item.table_name = item.get('table_name')
                    sql_function_condition_item.field_name = item.get('field_name')
                    sql_function_condition_item.value = item.get('value')
                    sql_function_condition_item.operator = item.get('operator')
                    sql_function_condition_item.relation = item.get('relation')
                    sql_function_condition_item.save()
                return responses.ok(data=serializer_sql_function.data, method=constant.PUT, entity_name='sql-function')
            except Exception as err:
                return responses.bad_request(data=str(err), message_code='UPDATE_SQL_FUNCTION_HAS_ERROR')
        else:
            return responses.bad_request(data=None, message_code='UPDATE_SQL_FUNCTION_INVALID')


class SqlFunctionDeleteView(DestroyAPIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    serializer_class = SwaggerSerializer
    queryset = SqlFunction.objects.all()

    @transaction.atomic()
    def delete(self, request, *args, **kwargs):
        sql_function_id = kwargs.get('pk')
        try:
            sql_function = self.get_queryset().get(id=sql_function_id)
            # Delete SqlFunctionOrderBy
            SqlFunctionOrderBy.objects.filter(sql_function__id=sql_function_id).delete()
            # Delete SqlFunctionMerge
            SqlFunctionMerge.objects.filter(sql_function__id=sql_function_id).delete()
            SqlFunctionConditionItems.objects.filter(sql_function_id=sql_function_id).delete()
            # Delete SqlFunction
            sql_function.delete()

            return responses.ok(data=None, method=constant.DELETE, entity_name='sql-function')
        except Exception as err:
            return responses.bad_request(data=str(err), message_code='DELETE_SQL_FUNCTION_HAS_ERROR')


class PreviewSqlFunctionView(ListAPIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    queryset = SqlFunction.objects.all()
    pagination_class = ResultsSetPagination
    serializer_class = SwaggerSerializer

    def list(self, request, *args, **kwargs):
        sql_function_id = kwargs.get('pk', None)
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 20)
        try:
            mongo_db_manager = MongoDBManager()
            sql_function = SqlFunction.objects.get(id=sql_function_id)
            connection = sql_function.connection
            if connection.name == MONGO:
                db, cache_db = mongo_db_manager.connection_mongo_by_provider(
                    provider_connection=connection)
                documents, count = mongo_db_manager.sql_function_exe(sql_function=sql_function, db=db, page=page,
                                                                     page_size=page_size)

                data = list(documents)
                result = json.loads(dumps(data))
                return responses.paging_data(data=result, total_count=count, method=constant.GET,
                                             entity_name='db_provider_connection')
            else:
                return responses.ok(data=None, method=constant.GET, entity_name='sql_function')
        except Exception as err:
            return responses.bad_request(data=str(err), message_code='SQL_ERROR')


class SqlJoinViewTest(ListAPIView):
    authentication_classes = []
    permission_classes = [AllowAny, ]
    queryset = DBProviderConnection.objects.all()
    serializer_class = SwaggerSerializer

    def get(self, request, *args, **kwargs):
        provider_connection = self.queryset.get(id=1)
        provider = provider_connection.provider
        if provider:
            if provider.name == MONGO:
                mongo_db_manager = MongoDBManager()
                db, cache_db = mongo_db_manager.connection_mongo_by_provider(provider_connection=provider_connection)
                collection = db['order_items']
                pipeline = [
                    {'$limit': 20},
                    {'$skip': 0},
                    {'$project': {'_id': 0}},
                    {
                        '$lookup': {
                            'from': 'order_reviews',
                            'localField': 'order_id',
                            'foreignField': 'order_id',
                            'as': 'data',
                        },
                    },
                    {
                        '$unwind': {
                            'path': '$data',
                            'preserveNullAndEmptyArrays': False
                        }
                    },
                    # {'$group': {
                    #     '_id': '$_id',
                    #     'data': {'$push': '$data'},
                    # }},
                    # {'$match': {
                    #     '$and': [
                    #         {'order_id': 'a548910a1c6147796b98fdf73dbeba33'},
                    #         {'data.review_id': '80e641a11e56f04c1ad469d5645fdfde'}
                    #     ]}},
                    {'$sort': {'order_id': -1}},
                    {
                        '$replaceRoot': {'newRoot': {'$mergeObjects': ['$data', '$$ROOT']}}
                    },
                    {
                        '$project': {'data': 0, '_id': 0}
                    }

                ]
                c = collection.aggregate(pipeline)
                data = list(c)
                result = json.loads(dumps(data))
                return responses.ok(data=result, method=constant.GET, entity_name='sql_function')


class SqlUnionViewTest(ListAPIView):
    authentication_classes = []
    permission_classes = [AllowAny, ]
    queryset = DBProviderConnection.objects.all()
    serializer_class = SwaggerSerializer

    def get(self, request, *args, **kwargs):
        provider_connection = self.queryset.get(id=1)
        provider = provider_connection.provider
        if provider:
            if provider.name == MONGO:
                mongo_db_manager = MongoDBManager()
                db, cache_db = mongo_db_manager.connection_mongo_by_provider(provider_connection=provider_connection)
                collection = db['order_items']

                pipeline = [
                    {'$limit': 1},  # Reduce the result set to a single document.
                    {'$project': {'_id': 1}},  # Strip all fields except the Id.
                    {'$project': {'_id': 0}},  # Strip the id. The document is now empty.
                    {'$lookup': {
                        'from': 'order_items',
                        'pipeline': [
                            {'$match': {
                                # 'date': {'$gte': ISODate('2018-09-01'), '$lte': ISODate('2018-09-10')},
                                # 'order_id': 'a548910a1c6147796b98fdf73dbeba33'
                                # 'price': {'$lte': {'$toInt':'810'}}
                                'order_item_id': '1'
                            }
                            },
                            {'$project': {
                                '_id': 0, 'result': '$price'
                            }}
                        ],
                        'as': 'collection1'
                    }},
                    {'$lookup': {
                        'from': 'order_reviews',
                        'pipeline': [
                            {'$match': {
                                # 'order_id': 'a548910a1c6147796b98fdf73dbeba33',
                                'review_score': '5'
                            }
                            },
                            {'$project': {
                                '_id': 0, 'result': '$review_score'
                            }}
                        ],

                        'as': 'collection2'
                    }},
                    {'$project': {
                        'Union': {'$setUnion': ['$collection1', '$collection2']}
                    }},
                    {'$unwind': '$Union'},  # Unwind the union collection into a result set.
                    {'$replaceRoot': {'newRoot': '$Union'}},  # Replace the root to cleanup the resulting documents.
                    # {'$limit': 20},
                    # {'$skip': 2*20},
                    # {'$sort': {'dated': -1}}
                ]
                c = collection.aggregate(pipeline)
                page = 1
                page_size = 20
                data = list(c)
                result = json.loads(dumps(data))
                start_length = 0 if page == 1 else (page - 1) * page_size + 1
                end_length = page_size if page == 1 else page * page_size + 1
                print(start_length)
                print(end_length)
                return responses.ok(data={'count': len(result), 'result': result[start_length:end_length]},
                                    method=constant.GET, entity_name='sql_function')
