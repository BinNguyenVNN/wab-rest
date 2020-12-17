from rest_framework import serializers

from wab.core.db_provider.models import DbProvider, DBProviderConnection


class DbProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = DbProvider
        fields = ["id", "name"]
        lookup_field = "id"


class DBProviderConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DBProviderConnection
        fields = ["id", "name", "host", "port", "username", "password", "provider", "ssl", "database"]
        lookup_field = "id"
