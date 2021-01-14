from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from wab.core.custom_column_fk.api.views import CustomColumnFKListView, CustomColumnFKCreateView, \
    CustomColumnFKUpdateView, CustomColumnFKDeleteView

# , PreviewCustomColumnFKView

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

app_name = "custom-column-fk"
urlpatterns = [
                  path('list-custom-column-fk/', CustomColumnFKListView.as_view(), name='CustomColumnFKListView'),
                  path("create-custom-column-fk/", CustomColumnFKCreateView.as_view(), name='CustomColumnFKCreateView'),
                  path('update-custom-column-fk/<int:pk>/', CustomColumnFKUpdateView.as_view(),
                       name='CustomColumnFKUpdateView'),
                  path('delete-custom-column-fk/<int:pk>/', CustomColumnFKDeleteView.as_view(),
                       name='CustomColumnFKDeleteView'),
                  # path("custom-column-fk/preview/<int:pk>/", PreviewCustomColumnFKView.as_view(),
                  #      name='PreviewCustomColumnFKView'),
              ] + router.urls
