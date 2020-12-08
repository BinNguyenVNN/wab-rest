from django.urls import include, path

urlpatterns = [
    path("users/", include("wab.core.users.urls")),
]
