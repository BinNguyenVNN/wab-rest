from rest_framework import serializers

from wab.core.custom_column.models import CustomColumnRegexType, CustomColumnType, \
    CustomColumnConfigValidation, CustomColumnTypeValidator
from wab.core.db_provider.api.serializers import DBProviderConnectionSerializer


class CustomColumnRegexTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomColumnRegexType
        fields = ["id", "name"]
        lookup_field = "id"


class CustomColumnTypeSerializer(serializers.ModelSerializer):
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


class CustomColumnTypeValidatorSerializer(serializers.ModelSerializer):
    custom_column_type = serializers.SerializerMethodField()
    custom_column_type_id = serializers.IntegerField(allow_null=True)

    custom_column_config_validation = serializers.SerializerMethodField()
    custom_column_config_validation_id = serializers.IntegerField(allow_null=True)

    custom_column_regex_type = serializers.SerializerMethodField()
    custom_column_regex_type_id = serializers.IntegerField(allow_null=True)

    def get_custom_column_type(self, obj):
        if obj.custom_column_type:
            serializer = CustomColumnTypeSerializer(obj.custom_column_type)
            return serializer.data
        return None

    def get_custom_column_regex_type_id(self, obj):
        return obj.custom_column_regex_type_id

    def get_custom_column_config_validation(self, obj):
        if obj.custom_column_config_validation:
            serializer = CustomColumnConfigValidationSerializer(obj.custom_column_config_validation)
            return serializer.data
        return None

    def get_custom_column_config_validation_id(self, obj):
        return obj.custom_column_config_validation_id

    def get_custom_column_regex_type(self, obj):
        if obj.custom_column_regex_type:
            serializer = CustomColumnRegexTypeSerializer(obj.custom_column_regex_type)
            return serializer.data
        return None

    def get_custom_column_regex_type_id(self, obj):
        return obj.custom_column_regex_type_id

    class Meta:
        model = CustomColumnTypeValidator
        fields = '__all__'
        lookup_field = "id"


class CustomColumnConfigValidationSerializer(serializers.ModelSerializer):
    custom_column_regex_type = serializers.SerializerMethodField()
    custom_column_regex_type_id = serializers.IntegerField(allow_null=True)

    def get_custom_column_regex_type(self, obj):
        if obj.custom_column_regex_type:
            serializer = CustomColumnRegexTypeSerializer(obj.custom_column_regex_type)
            return serializer.data
        return None

    def get_custom_column_regex_type_id(self, obj):
        return obj.custom_column_regex_type_id

    class Meta:
        model = CustomColumnConfigValidation
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
