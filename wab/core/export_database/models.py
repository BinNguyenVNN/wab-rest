from django.contrib.postgres.fields import ArrayField
from django.db import models
from wab.utils.jsonb import JSONField
from wab.core.db_provider.models import DBProviderConnection
from django.utils.translation import ugettext_lazy as _


class ExportData(models.Model):
    INIT, RUNNING, COMPLETE = ('init', 'running', 'complete')

    STATUS_CHOICES = (
        (INIT, _("init")),
        (RUNNING, _("running")),
        (COMPLETE, _("complete")),
    )

    EXCEL, TXT, PDF = ('excel', 'txt', 'pdf')

    FILE_TYPE = (
        (EXCEL, _("excel")),
        (TXT, _("txt")),
        (PDF, _("pdf")),
    )

    id = models.BigAutoField(primary_key=True)
    provider_connection = models.ForeignKey(DBProviderConnection, on_delete=models.CASCADE)
    username = models.CharField(max_length=128, blank=True, null=True)
    table = models.CharField(max_length=128, blank=True, null=True)
    file_path = models.CharField(max_length=128, blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES, default=INIT, max_length=20)
    file_type = models.CharField(choices=FILE_TYPE, default=TXT, max_length=20)
    list_filter = ArrayField(models.CharField(max_length=200), blank=True, null=True, default=list)
    list_column = ArrayField(models.CharField(max_length=200), blank=True, null=True, default=list)

    class Meta:
        db_table = 'export_data'
