from django.contrib.postgres.fields import ArrayField
from django.db import models
from wab.utils.jsonb import JSONField
from wab.core.db_provider.models import DBProviderConnection


class ImportData(models.Model):
    id = models.BigAutoField(primary_key=True)
    provider_connection = models.ForeignKey(DBProviderConnection, on_delete=models.CASCADE)
    username = models.CharField(max_length=128, blank=True, null=True)
    table = models.CharField(max_length=128, blank=True, null=True)
    record = ArrayField(JSONField(blank=True, null=True), blank=True, null=True, default=list)

    class Meta:
        db_table = 'import_data'
