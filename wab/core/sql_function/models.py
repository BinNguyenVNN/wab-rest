from enum import Enum

from django.db import models

from wab.core.db_provider.models import DBProviderConnection
from wab.core.models import BaseModel


class SqlFunction(BaseModel):
    name = models.CharField(null=True, blank=True, max_length=255)
    connection = models.ForeignKey(DBProviderConnection, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        return super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        db_table = 'sql_function'


class MERGE_TYPE(Enum):
    inner_join = ('inner_join', 'inner join')
    left_join = ('left_join', 'left join')
    right_join = ('right_join', 'right join')
    right_outer_join = ('right_outer_join', 'right outer join')
    union = ('union', 'union')

    @classmethod
    def get_value(cls, member):
        return cls[member].value[0]


class SqlFunctionMerge(BaseModel):
    table_name = models.CharField(null=True, blank=True, max_length=255)
    sql_function = models.ForeignKey(SqlFunction, on_delete=models.CASCADE, null=True, blank=True)

    merge_type = models.CharField(
        max_length=32,
        choices=[x.value for x in MERGE_TYPE],
        default=MERGE_TYPE.get_value('inner_join'),
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


class SqlFunctionCondition(BaseModel):
    sql_function = models.ForeignKey(SqlFunction, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.sql_function

    def save(self, *args, **kwargs):
        return super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        db_table = 'sql_function_condition'


class RELATION(Enum):
    relation_and = ('relation_and', 'and')
    relation_or = ('relation_or', 'or')

    @classmethod
    def get_value(cls, member):
        return cls[member].value[0]


class OPERATOR(Enum):
    type_equal = ('type_equal', '=')
    type_in = ('type_in', 'in')
    type_contain = ('type_contain', 'contain')

    @classmethod
    def get_value(cls, member):
        return cls[member].value[0]


class SqlFunctionConditionItems(BaseModel):
    table_name = models.CharField(null=True, blank=True, max_length=255)
    field_name = models.CharField(null=True, blank=True, max_length=255)

    operator = models.CharField(
        max_length=32,
        choices=[x.value for x in OPERATOR],
        default=OPERATOR.get_value('type_equal'),
    )
    value = models.CharField(null=True, blank=True, max_length=255)

    relation = models.CharField(
        max_length=32,
        choices=[x.value for x in RELATION],
        default=None,
    )

    sql_function_condition = models.ForeignKey(SqlFunctionCondition, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.relation

    def save(self, *args, **kwargs):
        return super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        db_table = 'sql_function_condition_items'
