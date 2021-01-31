from django.db import models

from wab.core.db_provider.models import DBProviderConnection


class ImportData(models.Model):
    id = models.BigAutoField(primary_key=True)
    provider_connection = models.ForeignKey(DBProviderConnection, on_delete=models.CASCADE)
    username = models.CharField(max_length=128, blank=True, null=True)
    table = models.CharField(max_length=128, blank=True, null=True)
    file_url = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        db_table = 'import_data'
