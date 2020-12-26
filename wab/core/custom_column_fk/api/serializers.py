from rest_framework import serializers
from wab.core.custom_column_fk.models import CustomColumnFK
from wab.core.db_provider.api.serializers import DBProviderConnectionSerializer


class CustomColumnFKSerializer(serializers.ModelSerializer):
    connection = serializers.SerializerMethodField()
    connection_id = serializers.IntegerField(allow_null=True)

    def get_connection(self, obj):
        if obj.connection:
            serializer = DBProviderConnectionSerializer(obj.connection)
            return serializer.data
        return None

    def get_connection_id(self, obj):
        return obj.connection_id

    class Meta:
        model = CustomColumnFK
        fields = '__all__'
        lookup_field = "id"

