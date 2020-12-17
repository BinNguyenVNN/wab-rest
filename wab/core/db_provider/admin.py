from django.contrib import admin

from wab.core.db_provider.models import DbProvider, DBProviderConnection


class DbProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'last_modified_by')


admin.site.register(DbProvider, DbProviderAdmin)


class DBProviderConnectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'host', 'port', 'database', 'username', 'password', 'provider', 'ssl')


admin.site.register(DBProviderConnection, DBProviderConnectionAdmin)
