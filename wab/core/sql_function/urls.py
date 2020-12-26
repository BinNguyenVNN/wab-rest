from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from wab.core.sql_function.api.views import SqlFunctionListView, SqlFunctionCreateView, SqlFunctionUpdateView, \
    SqlFunctionDeleteView, SqlJoinViewTest, SqlUnionViewTest

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

urlpatterns = [
                  path('test-join/', SqlJoinViewTest.as_view(),
                       name='SqlViewTest'),
                  path('test-union/', SqlUnionViewTest.as_view(),
                       name='SqlUnionViewTest'),
                  path('sql-function/list', SqlFunctionListView.as_view(),
                       name='SqlFunctionListView'),
                  path('sql-function/create', SqlFunctionCreateView.as_view(),
                       name='SqlFunctionCreateView'),
                  path('sql-function/update/<int:pk>', SqlFunctionUpdateView.as_view(),
                       name='SqlFunctionUpdateView'),
                  path('sql-function/delete/<int:pk>', SqlFunctionDeleteView.as_view(),
                       name='SqlFunctionDeleteView'),

              ] + router.urls