from rest_framework import serializers

from wab.core.db_provider.api.serializers import DBProviderConnectionSerializer
from wab.core.sql_function.models import SqlFunction, SqlFunctionOrderBy, SqlFunctionMerge, SqlFunctionConditionItems


class SqlFunctionSerializer(serializers.ModelSerializer):
    connection = serializers.SerializerMethodField()

    def get_connection(self, obj):
        if obj.connection:
            serializer = DBProviderConnectionSerializer(obj.connection)
            return serializer.data
        return None

    class Meta:
        model = SqlFunction
        fields = '__all__'


class SqlFunctionMergeSerializer(serializers.ModelSerializer):

    class Meta:
        model = SqlFunctionMerge
        fields = '__all__'


class SqlFunctionConditionItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = SqlFunctionConditionItems
        fields = '__all__'


class SqlFunctionDetailSerializer(serializers.ModelSerializer):
    connection = serializers.SerializerMethodField()
    sql_function_order_by_id = serializers.SerializerMethodField()
    order_by_name = serializers.SerializerMethodField()
    sql_function_merges = serializers.SerializerMethodField()
    sql_function_condition_items = serializers.SerializerMethodField()

    def get_connection(self, obj):
        if obj.connection:
            serializer = DBProviderConnectionSerializer(obj.connection)
            return serializer.data
        return None

    def get_sql_function_order_by_id(self, obj):
        sql_function_order_by = SqlFunctionOrderBy.objects.filter(sql_function=obj).first()
        if sql_function_order_by:
            return sql_function_order_by.id
        return None

    def get_order_by_name(self, obj):
        sql_function_order_by = SqlFunctionOrderBy.objects.filter(sql_function=obj).first()
        if sql_function_order_by:
            return sql_function_order_by.order_by_name
        return None

    def get_sql_function_merges(self, obj):
        sql_function_merges = SqlFunctionMerge.objects.filter(sql_function=obj)
        if sql_function_merges:
            serializer = SqlFunctionMergeSerializer(sql_function_merges, many=True)
            return serializer.data
        return []

    def get_sql_function_condition_items(self, obj):
        sql_function_condition_items = SqlFunctionConditionItems.objects.filter(sql_function=obj)
        if sql_function_condition_items:
            serializer = SqlFunctionConditionItemsSerializer(sql_function_condition_items, many=True)
            return serializer.data
        return []

    class Meta:
        model = SqlFunction
        fields = '__all__'
