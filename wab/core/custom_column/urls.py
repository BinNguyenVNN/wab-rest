from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from wab.core.custom_column.api.views import CustomColumnRegexTypeViewSet, CustomColumnTypeViewSet, \
    CustomColumnConfigTypeViewSet, CustomColumnConfigValidationViewSet, CustomColumnConfigTypeValidatorViewSet, \
    UpdateCustomColumnConfigTypeView

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("custom-column-regex-type", CustomColumnRegexTypeViewSet, basename="CustomColumnRegexTypeViewSet")
router.register("custom-column-config-type", CustomColumnConfigTypeViewSet, basename="CustomColumnConfigTypeViewSet")
router.register("custom-column-config-validation", CustomColumnConfigValidationViewSet,
                basename="CustomColumnConfigValidationViewSet")
router.register("custom-column-config-type-validator", CustomColumnConfigTypeValidatorViewSet,
                basename="CustomColumnConfigTypeValidatorViewSet")
router.register("custom-column-type", CustomColumnTypeViewSet, basename="CustomColumnTypeViewSet")

app_name = "custom-column"
urlpatterns = [
                  path('update-custom-column-config-type/<int:config_type_id>', UpdateCustomColumnConfigTypeView.as_view(),
                       name='UpdateCustomColumnConfigTypeView')
              ] + router.urls
