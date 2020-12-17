from rest_framework import serializers

from wab.core.custom_column.models import CustomColumnType, ValidationType, ValidationRegex, ColumnValidation


class CustomColumnTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomColumnType
        fields = ["id", "name", "type", "is_key"]
        lookup_field = "id"


class ValidationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValidationType
        fields = ["id", "name", "is_regex"]
        lookup_field = "id"


class ValidationRegexSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValidationRegex
        fields = ["id", "name"]
        lookup_field = "id"


class ListColumnValidationSerializer(serializers.ModelSerializer):
    custom_column_type = serializers.SerializerMethodField()
    validation_type = serializers.SerializerMethodField()
    validation_regex = serializers.SerializerMethodField()

    def get_custom_column_type(self, obj):
        if obj.custom_column_type:
            custom_column_type = CustomColumnType.objects.filter(id=obj.custom_column_type.id).first()
            if custom_column_type:
                return CustomColumnTypeSerializer(custom_column_type).data
            else:
                return None
        else:
            return None

    def get_validation_type(self, obj):
        if obj.validation_type:
            validation_type = ValidationType.objects.filter(id=obj.validation_type.id).first()
            if validation_type:
                return ValidationTypeSerializer(validation_type).data
            else:
                return None
        else:
            return None

    def get_validation_regex(self, obj):
        if obj.validation_regex:
            validation_regex = ValidationRegex.objects.filter(id=obj.validation_regex.id).first()
            if validation_regex:
                return ValidationRegexSerializer(validation_regex).data
            else:
                return None
        else:
            return None

    class Meta:
        model = ColumnValidation
        fields = '__all__'


class ColumnValidationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColumnValidation
        fields = ["id", "custom_column_type", "validation_type", "validation_regex", "name", "value", "regex",
                  "is_protect"]
