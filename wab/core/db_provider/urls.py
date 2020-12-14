from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from wab.core.db_provider.api.views import DbProviderViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("", DbProviderViewSet)

app_name = "db-provider"
urlpatterns = [

] + router.urls
