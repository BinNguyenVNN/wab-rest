from django.db import transaction
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from wab.core.sql_function.api.serializers import SqlFunctionSerializer
from wab.core.sql_function.models import SqlFunction, SqlFunctionOrderBy, SqlFunctionMerge, SqlFunctionCondition, \
    SqlFunctionConditionItems
from wab.utils import token_authentication, responses, constant


class SqlFunctionListView(ListAPIView):
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


class SqlFunctionCreateView(CreateAPIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    permission_classes = [AllowAny, ]
    serializer_class = SqlFunctionSerializer

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        data = request.data
        order_by_name = data.get("order_by_name")
        sql_function_merges = data.get("sql_function_merges")
        sql_function_condition_items = data.get("sql_function_condition_items")
        serializer_sql_function = self.get_serializer(data=data)
        if serializer_sql_function.is_valid(raise_exception=True):
            try:
                # Create SqlFunction
                data_sql_function = serializer_sql_function.save()
                sql_function = SqlFunction.objects.get(id=data_sql_function.id)

                # Create SqlFunctionOrderBy
                SqlFunctionOrderBy.objects.create(
                    order_by_name=order_by_name,
                    sql_function=sql_function
                )
                # Create SqlFunctionMerge
                for sql_function_merge in sql_function_merges:
                    SqlFunctionMerge.objects.create(
                        table_name=sql_function_merge.get("table_name"),
                        merge_type=sql_function_merge.get("merge_type"),
                        sql_function=sql_function
                    )

                # Create SqlFunctionCondition
                sql_function_condition = SqlFunctionCondition.objects.create(
                    sql_function=sql_function
                )

                # Create SqlFunctionConditionItems
                for sql_function_condition_item in sql_function_condition_items:
                    SqlFunctionConditionItems.objects.create(
                        table_name=sql_function_condition_item.get("table_name"),
                        field_name=sql_function_condition_item.get("field_name"),
                        sql_function_condition=sql_function_condition,
                        value=sql_function_condition_item.get("value"),
                        operator=sql_function_condition_item.get("operator"),
                        relation=sql_function_condition_item.get("relation")
                    )

                return responses.ok(data=serializer_sql_function.data, method=constant.POST, entity_name='sql-function')
            except Exception as err:
                return responses.bad_request(data=None, message_code='CREATE_SQL_FUNCTION_HAS_ERROR',
                                             message_system=err)
        else:
            return responses.bad_request(data=None, message_code='CREATE_SQL_FUNCTION_INVALID')


class SqlFunctionUpdateView(UpdateAPIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    permission_classes = [AllowAny, ]
    serializer_class = SqlFunctionSerializer

    @transaction.atomic()
    def put(self, request, *args, **kwargs):
        sql_function_id = kwargs.get("pk")
        data = request.data
        order_by_name = data.get("order_by_name")
        sql_function_merges = data.get("sql_function_merges")
        sql_function_condition_items = data.get("sql_function_condition_items")
        serializer_sql_function = self.get_serializer(data=data)
        if serializer_sql_function.is_valid(raise_exception=True):
            try:
                # Update SqlFunction
                sql_function = SqlFunction.objects.get(id=sql_function_id)
                serializer_sql_function = self.get_serializer(data=sql_function)
                data_sql_function = serializer_sql_function.save()

                # Update SqlFunctionOrderBy
                SqlFunctionOrderBy.objects.update(
                    order_by_name=order_by_name,
                    sql_function=sql_function
                )
                # Update SqlFunctionMerge
                for sql_function_merge in sql_function_merges:
                    SqlFunctionMerge.objects.update(
                        table_name=sql_function_merge.get("table_name"),
                        merge_type=sql_function_merge.get("merge_type"),
                        sql_function=sql_function
                    )

                # Update SqlFunctionCondition
                sql_function_condition = SqlFunctionCondition.objects.update(
                    sql_function=sql_function
                )

                # Update SqlFunctionConditionItems
                for sql_function_condition_item in sql_function_condition_items:
                    SqlFunctionConditionItems.objects.update(
                        table_name=sql_function_condition_item.get("table_name"),
                        field_name=sql_function_condition_item.get("field_name"),
                        sql_function_condition=sql_function,
                        value=sql_function_condition_item.get("value"),
                        operator=sql_function_condition_item.get("operator"),
                        relation=sql_function_condition_item.get("relation")
                    )

                return responses.ok(data=serializer_sql_function.data, method=constant.PUT, entity_name='sql-function')
            except Exception as err:
                return responses.bad_request(data=None, message_code='UPDATE_SQL_FUNCTION_HAS_ERROR',
                                             message_system=err)
        else:
            return responses.bad_request(data=None, message_code='UPDATE_SQL_FUNCTION_INVALID')


class SqlFunctionDeleteView(DestroyAPIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    permission_classes = [AllowAny, ]

    @transaction.atomic()
    def delete(self, request, *args, **kwargs):
        sql_function_id = kwargs.get("pk")
        try:
            sql_function = SqlFunction.objects.get(id=sql_function_id)

            # Delete SqlFunctionOrderBy
            sql_function_order_bys = SqlFunctionOrderBy.objects.all()
            for sql_function_order_by in sql_function_order_bys:
                sql_function_order_by.delete()

            # Delete SqlFunctionMerge
            sql_function_merges = SqlFunctionMerge.objects.filter(sql_function__id=sql_function_id)
            for sql_function_merge in sql_function_merges:
                sql_function_merge.delete()

            sql_function_conditions = SqlFunctionCondition.objects.filter(sql_function__id=sql_function_id)
            sql_function_condition = None
            for item in sql_function_conditions:
                sql_function_condition = item
                break

            # Delete SqlFunctionConditionItems
            if sql_function_condition is not None:
                sql_function_condition_items = SqlFunctionConditionItems.objects.filter(
                    sql_function_condition__id=sql_function_condition.id)
                for sql_function_condition_item in sql_function_condition_items:
                    sql_function_condition_item.delete()

                # Delete SqlFunctionCondition
                sql_function_condition.delete()

            # Delete SqlFunction
            sql_function.delete()

            return responses.ok(data=None, method=constant.DELETE, entity_name='sql-function')
        except Exception as err:
            return responses.bad_request(data=None, message_code='DELETE_SQL_FUNCTION_HAS_ERROR',
                                         message_system=err)
