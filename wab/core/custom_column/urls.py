from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from wab.core.custom_column.api.views import CustomColumnTypeViewSet, \
    CustomColumnConfigValidationViewSet, \
    UpdateCustomColumnTypeView, CreateCustomColumnMappingView, UpdateCustomColumnMappingView, ConvertData, \
    CustomColumnValidatorListByCustomColumnIdView, CreateCustomColumnTypeView

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("custom-column-config-validation", CustomColumnConfigValidationViewSet,
                basename="CustomColumnConfigValidationViewSet")
router.register("custom-column-type", CustomColumnTypeViewSet, basename="CustomColumnTypeViewSet")

app_name = "custom-column"
urlpatterns = [
                  path('create-custom-column-type/', CreateCustomColumnTypeView.as_view(),
                       name='CreateCustomColumnTypeView'),
                  path('update-custom-column-type/<int:custom_column_type_id>/', UpdateCustomColumnTypeView.as_view(),
                       name='UpdateCustomColumnTypeView'),
                  path('list-custom-column-type-validator/<int:custom_column_type_id>/',
                       CustomColumnValidatorListByCustomColumnIdView.as_view(),
                       name='UpdateCustomColumnTypeView'),
                  path('custom-column-mapping/', CreateCustomColumnMappingView.as_view(),
                       name='CreateCustomColumnMappingView'),
                  path('custom-column-mapping/<int:pk>/', UpdateCustomColumnMappingView.as_view(),
                       name='UpdateCustomColumnMappingView'),
                  path("convert/", ConvertData.as_view(), name='ConvertData'),
              ] + router.urls
