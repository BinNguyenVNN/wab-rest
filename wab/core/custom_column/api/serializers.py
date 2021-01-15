from rest_framework import serializers

from wab.core.custom_column.models import CustomColumnType, \
    CustomColumnConfigValidation, CustomColumnTypeValidator, CustomColumnMapping
from wab.core.db_provider.api.serializers import DBProviderConnectionSerializer


class CustomColumnTypeSerializer(serializers.ModelSerializer):
    connection = serializers.SerializerMethodField()
    connection_id = serializers.IntegerField(allow_null=True)
    validations = serializers.SerializerMethodField()

    def get_connection(self, obj):
        if obj.connection:
            serializer = DBProviderConnectionSerializer(obj.connection)
            return serializer.data
        return None

    def get_validations(self, obj):
        if obj.connection:
            serializer = CustomColumnTypeValidatorSerializer(obj.custom_column_type_validations.all(), many=True)
            return serializer.data
        return None

    def get_connection_id(self, obj):
        return obj.connection_id

    class Meta:
        model = CustomColumnType
        fields = '__all__'
        lookup_field = "id"


class CustomColumnTypeValidatorSerializer(serializers.ModelSerializer):
    custom_column_config_validation = serializers.SerializerMethodField()

    def get_custom_column_config_validation(self, obj):
        if obj.custom_column_config_validation:
            serializer = CustomColumnConfigValidationSerializer(obj.custom_column_config_validation)
            return serializer.data
        return None

    class Meta:
        model = CustomColumnTypeValidator
        fields = '__all__'
        lookup_field = "id"


class CustomColumnConfigValidationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomColumnConfigValidation
        fields = '__all__'
        lookup_field = "id"


class CreateCustomColumnTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomColumnType
        fields = '__all__'
        lookup_field = "id"


class UpdateCustomColumnTypeSerializer(serializers.ModelSerializer):
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
        model = CustomColumnType
        fields = '__all__'
        lookup_field = "id"


class CreateCustomColumnMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomColumnMapping
        fields = '__all__'
