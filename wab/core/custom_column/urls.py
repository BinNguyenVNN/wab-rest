from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from wab.core.custom_column.api.views import CustomColumnRegexTypeViewSet, CustomColumnTypeViewSet, \
    CustomColumnConfigTypeViewSet, CustomColumnConfigValidationViewSet, CustomColumnConfigTypeValidatorViewSet

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
                  # path('validation-list/<int:custom_column_type_id>', ColumnValidationListView.as_view(),
                  #      name='ColumnValidationListView'),
                  # path('validation-create/<int:custom_column_type_id>', ColumnValidationCreateView.as_view(),
                  #      name='ColumnValidationCreateView'),
                  # path('validation-update/<int:custom_column_type_id>', ColumnValidationUpdateView.as_view(),
                  #      name='ColumnValidationUpdateView')
              ] + router.urls
