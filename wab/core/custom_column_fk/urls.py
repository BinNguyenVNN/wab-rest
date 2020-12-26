from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from wab.core.custom_column_fk.api.views import CustomColumnFKViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("custom-column-fk", CustomColumnFKViewSet, basename="CustomColumnFKViewSet")


app_name = "custom-column-fk"
urlpatterns = [

              ] + router.urls
