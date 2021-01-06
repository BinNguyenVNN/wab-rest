from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from wab.core.custom_column_fk.api.views import CustomColumnFKViewSet, ListOperatorMongoDBView

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("custom-column-fk", CustomColumnFKViewSet, basename="CustomColumnFKViewSet")

app_name = "custom-column-fk"
urlpatterns = [
                  path("list-operator-mongodb/", ListOperatorMongoDBView.as_view(), name='ListOperatorMongoDBView')
              ] + router.urls
