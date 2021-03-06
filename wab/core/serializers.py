from rest_framework import serializers


class SwaggerSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class SwaggerConvertDataSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    provider_connection_id = serializers.IntegerField()
    table = serializers.CharField()
    convert_field = serializers.CharField()
    data_type = serializers.CharField()
