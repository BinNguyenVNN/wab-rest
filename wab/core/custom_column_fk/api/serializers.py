from rest_framework import serializers

from wab.core.custom_column_fk.models import CustomColumnFK, CustomColumnFKFilter
from wab.core.db_provider.api.serializers import DBProviderConnectionSerializer


class CustomColumnFKFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomColumnFKFilter
        fields = '__all__'
        lookup_field = "id"


class CustomColumnFKSerializer(serializers.ModelSerializer):
    connection = serializers.SerializerMethodField()
    list_filters = serializers.SerializerMethodField()

    def get_connection(self, obj):
        if obj.connection:
            serializer = DBProviderConnectionSerializer(obj.connection)
            return serializer.data
        return None

    def get_list_filters(self, obj):
        if obj.connection:
            serializer = CustomColumnFKFilterSerializer(obj.custom_column_fk_filters.all(), many=True)
            return serializer.data
        else:
            return []

    class Meta:
        model = CustomColumnFK
        fields = '__all__'
        lookup_field = "id"
