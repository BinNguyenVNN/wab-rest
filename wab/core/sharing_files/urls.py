from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from wab.core.sharing_files.api.views import SharingFilesGetLinkView, SharingFilesGetDataView

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

urlpatterns = [
                  path('create-link/<str:connection_id>/<str:table_name>/', SharingFilesGetLinkView.as_view(),
                       name='SharingFilesCreateLinkView'),
                  path('get-data/<str:sharing_key>/', SharingFilesGetDataView.as_view(),
                       name='SharingFilesGetDataView')

              ] + router.urls
