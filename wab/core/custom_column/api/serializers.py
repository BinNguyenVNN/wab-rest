from rest_framework import serializers

from wab.core.custom_column.models import CustomColumnRegexType, CustomColumnType, CustomColumnConfigType, \
    CustomColumnConfigValidation, CustomColumnConfigTypeValidator


class CustomColumnRegexTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomColumnRegexType
        fields = ["id", "name"]
        lookup_field = "id"


class CustomColumnConfigTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomColumnConfigType
        fields = ["id", "name"]
        lookup_field = "id"


class CustomColumnConfigTypeValidatorSerializer(serializers.ModelSerializer):
    custom_column_config_type = serializers.SerializerMethodField()
    custom_column_config_validation = serializers.SerializerMethodField()
    custom_column_regex_type = serializers.SerializerMethodField()

    def get_custom_column_config_type(self, obj):
        if obj.custom_column_config_type:
            serializer = CustomColumnConfigTypeSerializer(obj.custom_column_config_type)
            return serializer.data
        return None

    def get_custom_column_config_validation(self, obj):
        if obj.custom_column_config_validation:
            serializer = CustomColumnConfigValidationSerializer(obj.custom_column_config_validation)
            return serializer.data
        return None

    def get_custom_column_regex_type(self, obj):
        if obj.custom_column_regex_type:
            serializer = CustomColumnRegexTypeSerializer(obj.custom_column_regex_type)
            return serializer.data
        return None

    class Meta:
        model = CustomColumnConfigTypeValidator
        fields = ["id", "name", "custom_column_config_type", "custom_column_config_validation",
                  "custom_column_regex_type", "value"]
        lookup_field = "id"


class CustomColumnConfigValidationSerializer(serializers.ModelSerializer):
    custom_column_regex_type = serializers.SerializerMethodField()

    def get_custom_column_regex_type(self, obj):
        if obj.custom_column_regex_type:
            serializer = CustomColumnRegexTypeSerializer(obj.custom_column_regex_type)
            return serializer.data
        return None

    class Meta:
        model = CustomColumnConfigValidation
        fields = ["id", "name", "is_protect", "custom_column_regex_type", "function"]
        lookup_field = "id"


class CustomColumnTypeSerializer(serializers.ModelSerializer):
    custom_column_config_type = serializers.SerializerMethodField()

    def get_custom_column_config_type(self, obj):
        if obj.custom_column_config_type:
            serializer = CustomColumnConfigTypeSerializer(obj.custom_column_config_type)
            return serializer.data
        return None

    class Meta:
        model = CustomColumnType
        fields = ["id", "name", "custom_column_config_type", "is_key"]
        lookup_field = "id"
