from enum import Enum
from django.db import models
from wab.core.db_provider.models import DBProviderConnection
from wab.core.models import BaseModel


class OPERATOR(Enum):
    operator_in = ('in', 'in')
    operator_contain = ('contain', 'contain')

    @classmethod
    def get_value(cls, member):
        return cls[member].value[0]


class CustomColumnFK(BaseModel):
    connection = models.ForeignKey(DBProviderConnection, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(null=True, blank=True, max_length=255)
    table_name = models.CharField(null=True, blank=True, max_length=255)
    field_name = models.CharField(null=True, blank=True, max_length=255)
    operator = models.CharField(
        max_length=32,
        choices=[x.value for x in OPERATOR],
        default=OPERATOR.get_value('operator_contain'),
        null=True,
        blank=True
    )
    value = models.CharField(null=True, blank=True, max_length=255)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        return super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        db_table = 'custom_column_fk'
