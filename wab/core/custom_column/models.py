from django.db import models

from wab.core.models import BaseModel


class CustomColumnRegexType(BaseModel):
    name = models.CharField(null=True, blank=True, max_length=255)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        return super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        db_table = 'custom_column_regex_type'


class CustomColumnConfigValidation(BaseModel):
    name = models.CharField(null=True, blank=True, max_length=255)
    is_protect = models.BooleanField(default=False)
    custom_column_regex_type = models.ForeignKey(CustomColumnRegexType, on_delete=models.CASCADE, null=True, blank=True)
    function = models.CharField(null=True, blank=True, max_length=255)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        return super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        db_table = 'custom_column_config_validation'


class CustomColumnConfigType(BaseModel):
    name = models.CharField(null=True, blank=True, max_length=255)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        return super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        db_table = 'custom_column_config_type'


class CustomColumnConfigTypeValidator(BaseModel):
    customer_column_config_type = models.ForeignKey(CustomColumnConfigType, on_delete=models.CASCADE, null=True,
                                                    blank=True)
    customer_column_config_validation = models.ForeignKey(CustomColumnConfigValidation, on_delete=models.CASCADE,
                                                          null=True, blank=True)
    name = models.CharField(null=True, blank=True, max_length=255)
    value = models.CharField(null=True, blank=True, max_length=255)
    custom_column_regex_type = models.ForeignKey(CustomColumnRegexType, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        return super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        db_table = 'custom_column_config_type_validator'


class CustomColumnType(BaseModel):
    name = models.CharField(null=True, blank=True, max_length=255)
    is_key = models.BooleanField(default=True)
    customer_column_config_type = models.ForeignKey(CustomColumnConfigType, on_delete=models.CASCADE, null=True,
                                                    blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        return super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        db_table = 'custom_column_type'
