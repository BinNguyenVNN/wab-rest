from django.db import models

from wab.core.db_provider.models import DBProviderConnection
from wab.core.models import BaseModel
from wab.utils.operator import RegexType, OperatorMongo


class CustomColumnConfigValidation(BaseModel):
    name = models.CharField(null=True, blank=True, max_length=255)
    is_protect = models.BooleanField(default=False)
    is_regex = models.BooleanField(default=False)
    regex = models.CharField(
        max_length=32,
        choices=[x.value for x in RegexType],
        default=None,
        null=True,
        blank=True
    )
    function = models.CharField(null=True, blank=True, max_length=255)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        return super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        db_table = 'custom_column_config_validation'


class CustomColumnType(BaseModel):
    name = models.CharField(null=True, blank=True, max_length=255)
    is_key = models.BooleanField(default=True)
    slug = models.CharField(null=True, blank=True, max_length=255)
    connection = models.ForeignKey(DBProviderConnection, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        return super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        db_table = 'custom_column_type'


class CustomColumnTypeValidator(BaseModel):
    custom_column_type = models.ForeignKey(CustomColumnType, on_delete=models.CASCADE, null=True, blank=True,
                                           related_name='custom_column_type_validations')
    custom_column_config_validation = models.ForeignKey(CustomColumnConfigValidation, on_delete=models.CASCADE,
                                                        null=True, blank=True)
    name = models.CharField(null=True, blank=True, max_length=255)
    operator = models.CharField(
        max_length=32,
        choices=[x.value for x in OperatorMongo],
        default=OperatorMongo.get_value('operator_equals'),
        null=True,
        blank=True
    )
    value = models.CharField(null=True, blank=True, max_length=255)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        return super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        db_table = 'custom_column_type_validator'


class CustomColumnMapping(models.Model):
    connection = models.ForeignKey(DBProviderConnection, on_delete=models.CASCADE, null=True, blank=True)
    table_name = models.CharField(null=True, blank=True, max_length=255)
    real_column = models.CharField(null=True, blank=True, max_length=255)
    custom_column_name = models.CharField(null=True, blank=True, max_length=255)
    custom_column = models.ForeignKey(CustomColumnType, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.custom_column_name

    class Meta:
        db_table = 'custom_column_mapping'


class CustomColumnTaskConvert(models.Model):
    connection = models.ForeignKey(DBProviderConnection, on_delete=models.CASCADE, null=True, blank=True)
    table_name = models.CharField(null=True, blank=True, max_length=255)
    column_name = models.CharField(null=True, blank=True, max_length=255)
    data_real_type = models.CharField(null=True, blank=True, max_length=255)
    data_type = models.CharField(null=True, blank=True, max_length=255)
    current_row = models.IntegerField(default=0)

    class Meta:
        db_table = 'custom_column_task_convert'
