from django.contrib import admin

from wab.core.db_provider.models import DbProvider


class DbProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'prefix', 'creator', 'last_modified_by')


admin.site.register(DbProvider, DbProviderAdmin)

