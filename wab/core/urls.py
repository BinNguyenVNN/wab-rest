from django.urls import include, path

from wab.core.export_database.views import ExportPdfView, ExportExcelView, ExportTextView

urlpatterns = [
    path("users/", include("wab.core.users.urls")),
    path("", include("wab.core.custom_column.urls")),
    path("db-provider/", include("wab.core.db_provider.urls")),
    path("sql-function/", include("wab.core.sql_function.urls")),
    path("export/pdf/<int:connction>/<str:table_name>/", ExportPdfView.as_view(), name="export-pdf"),
    path("export/excel/<int:connction>/<str:table_name>/", ExportExcelView.as_view(), name="export-excel"),
    path("export/text/<int:connction>/<str:table_name>/", ExportTextView.as_view(), name="export-text"),
]
