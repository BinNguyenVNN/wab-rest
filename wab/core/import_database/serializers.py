from rest_framework import serializers


class ImportCsvSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    table_name = serializers.CharField()
    is_existed = serializers.BooleanField()
