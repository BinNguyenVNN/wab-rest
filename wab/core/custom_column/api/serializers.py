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
    custom_column_config_type_id = serializers.IntegerField(allow_null=True)

    custom_column_config_validation = serializers.SerializerMethodField()
    custom_column_config_validation_id = serializers.IntegerField(allow_null=True)

    custom_column_regex_type = serializers.SerializerMethodField()
    custom_column_regex_type_id = serializers.IntegerField(allow_null=True)

    def get_custom_column_config_type(self, obj):
        if obj.custom_column_config_type:
            serializer = CustomColumnConfigTypeSerializer(obj.custom_column_config_type)
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
        model = CustomColumnConfigTypeValidator
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


class CustomColumnTypeSerializer(serializers.ModelSerializer):
    custom_column_config_type = serializers.SerializerMethodField()
    custom_column_config_type_id = serializers.IntegerField(allow_null=True)

    def get_custom_column_config_type(self, obj):
        if obj.custom_column_config_type:
            serializer = CustomColumnConfigTypeSerializer(obj.custom_column_config_type)
            return serializer.data
        return None

    def get_custom_column_config_type_id(self, obj):
        return obj.custom_column_config_type_id

    class Meta:
        model = CustomColumnType
        fields = '__all__'
        lookup_field = "id"
