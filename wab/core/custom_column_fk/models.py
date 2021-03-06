from django.db import models

from wab.core.db_provider.models import DBProviderConnection
from wab.core.models import BaseModel
from wab.utils.operator import OperatorMongo


class CustomColumnFK(BaseModel):
    connection = models.ForeignKey(DBProviderConnection, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(null=True, blank=True, max_length=255)
    table_name = models.CharField(null=True, blank=True, max_length=255)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        return super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        db_table = 'custom_column_fk'


class CustomColumnFKFilter(BaseModel):
    field_name = models.CharField(null=True, blank=True, max_length=255)
    operator = models.CharField(
        max_length=32,
        choices=[x.value for x in OperatorMongo],
        default=OperatorMongo.get_value('operator_equals'),
        null=True,
        blank=True
    )
    value = models.CharField(null=True, blank=True, max_length=255)
    custom_column_fk = models.ForeignKey(CustomColumnFK, on_delete=models.CASCADE, null=True, blank=True,
                                         related_name='custom_column_fk_filters')

    def __str__(self):
        return self.field_name

    def save(self, *args, **kwargs):
        return super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        db_table = 'custom_column_fk_filter'
