from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from wab.core.sql_function.api.views import SqlViewTest

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

urlpatterns = [
                  path('test/', SqlViewTest.as_view(),
                       name='SqlViewTest'),

              ] + router.urls
