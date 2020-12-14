from rest_framework import serializers

from wab.core.db_provider.models import DbProvider


class DbProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = DbProvider
        fields = ["id", "name"]
        lookup_field = "id"
