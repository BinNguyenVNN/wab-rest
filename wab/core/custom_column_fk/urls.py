from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from wab.core.custom_column_fk.api.views import CustomColumnFKViewSet,PreviewCustomColumnFKView

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("custom-column-fk", CustomColumnFKViewSet, basename="CustomColumnFKViewSet")

app_name = "custom-column-fk"
urlpatterns = [
                  path("custom-column-fk/preview/<int:pk>/", PreviewCustomColumnFKView.as_view(),
                       name='PreviewCustomColumnFKView'),
              ] + router.urls
