from django.contrib import admin
from wab.core.users.models import User, KeyModel


class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'username', 'email', 'is_active', 'password')


admin.site.register(User, UserAdmin)


class KeyModelAdmin(admin.ModelAdmin):
    list_display = ('key', 'user', 'created')


admin.site.register(KeyModel, KeyModelAdmin)
