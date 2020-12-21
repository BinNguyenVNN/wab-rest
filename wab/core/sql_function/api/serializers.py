from rest_framework import serializers

from wab.core.db_provider.api.serializers import DBProviderConnectionSerializer
from wab.core.sql_function.models import SqlFunction


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
