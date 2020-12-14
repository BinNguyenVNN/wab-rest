from django.db import models

from wab.core.models import BaseModel


class CustomColumnType(BaseModel):
    name = models.CharField(null=True, blank=True, max_length=255)
    type = models.TextField(null=True, blank=True)
    is_key = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        return super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        db_table = 'custom_column_type'


class ValidationType(BaseModel):
    name = models.CharField(null=True, blank=True, max_length=255)
    is_regex = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        return super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        db_table = 'validation_type'


class ValidationRegex(BaseModel):
    name = models.CharField(null=True, blank=True, max_length=255)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        return super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        db_table = 'validation_regex'


class ColumnValidation(BaseModel):
    custom_column_type = models.ForeignKey(CustomColumnType, null=True, blank=True, on_delete=models.CASCADE)
    validation_type = models.ForeignKey(ValidationType, null=True, blank=True, on_delete=models.CASCADE)
    validation_regex = models.ForeignKey(ValidationRegex, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(null=True, blank=True, max_length=255)
    value = models.CharField(null=True, blank=True, max_length=255)
    regex = models.CharField(null=True, blank=True, max_length=255)
    is_protect = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        return super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        db_table = 'column_validation'
