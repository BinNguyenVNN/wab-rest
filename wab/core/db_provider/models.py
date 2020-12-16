from django.db import models

from wab.core.models import BaseModel


class DbProvider(BaseModel):
    name = models.CharField(null=True, blank=True, max_length=255)
    # prefix = models.CharField(null=True, blank=True, max_length=128)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        return super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        db_table = 'db_provider'


class DBProviderConnection(BaseModel):
    name = models.CharField(null=True, blank=True, max_length=255)
    host = models.CharField(null=True, blank=True, max_length=255)
    port = models.IntegerField(default=0)
    database = models.CharField(null=True, blank=True, max_length=128)
    username = models.CharField(null=True, blank=True, max_length=128)
    password = models.CharField(null=True, blank=True, max_length=255)
    provider = models.ForeignKey(DbProvider, on_delete=models.CASCADE, null=True, blank=True)
    ssl = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        return super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        db_table = 'db_provider_connection'
