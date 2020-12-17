from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from wab.core.custom_column.api.views import CustomColumnTypeViewSet, ValidationTypeViewSet, ValidationRegexViewSet, \
    ColumnValidationListView, ColumnValidationCreateView, ColumnValidationUpdateView

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("custom-column-type", CustomColumnTypeViewSet, basename="CustomColumnTypeViewSet")
router.register("validation-type", ValidationTypeViewSet, basename="ValidationTypeViewSet")
router.register("validation-regex", ValidationRegexViewSet, basename="ValidationRegexViewSet")

# app_name = "custom-column"
urlpatterns = [
                  path('validation-list/<int:custom_column_type_id>', ColumnValidationListView.as_view(),
                       name='ColumnValidationListView'),
                  path('validation-create/<int:custom_column_type_id>', ColumnValidationCreateView.as_view(),
                       name='ColumnValidationCreateView'),
                  path('validation-update/<int:custom_column_type_id>', ColumnValidationUpdateView.as_view(),
                       name='ColumnValidationUpdateView')
              ] + router.urls
