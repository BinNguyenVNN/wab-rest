from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from wab.core.sql_function.api.views import SqlFunctionListView, SqlFunctionCreateView, SqlFunctionUpdateView, \
    SqlFunctionDeleteView, SqlJoinViewTest, SqlUnionViewTest, PreviewSqlFunctionView, SqlFunctionDetailView

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

urlpatterns = [
                  path('test-join/', SqlJoinViewTest.as_view(), name='SqlViewTest'),
                  path('test-union/', SqlUnionViewTest.as_view(), name='SqlUnionViewTest'),
                  path('list/', SqlFunctionListView.as_view(), name='SqlFunctionListView'),
                  path('create/', SqlFunctionCreateView.as_view(), name='SqlFunctionCreateView'),
                  path('detail/<int:pk>/', SqlFunctionDetailView.as_view(), name='SqlFunctionUpdateView'),
                  path('update/<int:pk>/', SqlFunctionUpdateView.as_view(), name='SqlFunctionUpdateView'),
                  path('delete/<int:pk>/', SqlFunctionDeleteView.as_view(), name='SqlFunctionDeleteView'),
                  path('preview/<int:pk>/', PreviewSqlFunctionView.as_view(),
                       name='PreviewSqlFunctionView'),

              ] + router.urls
