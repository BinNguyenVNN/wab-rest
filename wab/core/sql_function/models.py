from django.db import models

from wab.core.db_provider.models import DBProviderConnection
from wab.core.models import BaseModel
from wab.utils.operator import OPERATOR_MONGODB, MERGE_TYPE, RELATION


class SqlFunction(BaseModel):
    name = models.CharField(null=True, blank=True, max_length=255)
    connection = models.ForeignKey(DBProviderConnection, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        return super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        db_table = 'sql_function'


class SqlFunctionMerge(BaseModel):
    table_name = models.CharField(null=True, blank=True, max_length=255)
    column_name = models.CharField(null=True, blank=True, max_length=255)
    sql_function = models.ForeignKey(SqlFunction, on_delete=models.CASCADE, null=True, blank=True)

    merge_type = models.CharField(
        max_length=32,
        choices=[x.value for x in MERGE_TYPE],
        default=None,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.merge_type

    def save(self, *args, **kwargs):
        return super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        db_table = 'sql_function_merge'


class SqlFunctionOrderBy(BaseModel):
    order_by_name = models.CharField(null=True, blank=True, max_length=255)
    sql_function = models.ForeignKey(SqlFunction, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.order_by_name

    def save(self, *args, **kwargs):
        return super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        db_table = 'sql_function_order_by'


# class SqlFunctionCondition(BaseModel):
#     sql_function = models.ForeignKey(SqlFunction, on_delete=models.CASCADE, null=True, blank=True)
#
#     def __str__(self):
#         return self.sql_function.name
#
#     def save(self, *args, **kwargs):
#         return super(BaseModel, self).save(*args, **kwargs)
#
#     class Meta:
#         db_table = 'sql_function_condition'


class SqlFunctionConditionItems(BaseModel):
    table_name = models.CharField(null=True, blank=True, max_length=255)
    field_name = models.CharField(null=True, blank=True, max_length=255)

    operator = models.CharField(
        max_length=32,
        choices=[x.value for x in OPERATOR_MONGODB],
        default=None,
        null=True,
        blank=True
    )
    value = models.CharField(null=True, blank=True, max_length=255)

    relation = models.CharField(
        max_length=32,
        choices=[x.value for x in RELATION],
        default=None,
        null=True,
        blank=True
    )

    sql_function = models.ForeignKey(SqlFunction, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.relation

    def save(self, *args, **kwargs):
        return super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        db_table = 'sql_function_condition_items'
