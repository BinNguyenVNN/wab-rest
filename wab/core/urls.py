from django.urls import include, path

urlpatterns = [
    path("users/", include("wab.core.users.urls")),
    path("", include("wab.core.custom_column.urls")),
    path("db-provider/", include("wab.core.db_provider.urls")),
]
