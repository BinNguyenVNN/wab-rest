from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from wab.core.db_provider.api.views import DbProviderViewSet, DBProviderConnectionViewSet, DBConnectionConnectView, \
    DBConnectionListTableView, DBConnectionListColumnView, DBConnectionListDataView, CheckView

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("db-provider", DbProviderViewSet, basename="DbProviderViewSet")
router.register("connection", DBProviderConnectionViewSet, basename="DBProviderConnectionViewSet")
# app_name = "db-provider"
urlpatterns = [
                  path('connection/connect/', DBConnectionConnectView.as_view(),
                       name='DBConnectionCreateView'),
                  path('connection/tables/<int:pk>/', DBConnectionListTableView.as_view(),
                       name='DBConnectionCreateView'),
                  path('connection/columns/<int:pk>/<str:table>/', DBConnectionListColumnView.as_view(),
                       name='DBConnectionListColumnView'),
                  path('connection/documents/<int:pk>/<str:table>/', DBConnectionListDataView.as_view(),
                       name='DBConnectionListDataView'),

                  path('connection/check/', CheckView.as_view(),
                       name='CheckView'),

              ] + router.urls
