from django.urls import include, path

from wab.core.export_database.views import ExportPdfView, ExportExcelView, ExportTextView
from wab.core.import_database.views import ImportCsvView

urlpatterns = [
    path("users/", include("wab.core.users.urls")),
    path("", include("wab.core.custom_column.urls")),
    path("db-provider/", include("wab.core.db_provider.urls")),
    path("sql-function/", include("wab.core.sql_function.urls")),
    path("export/pdf/<int:connection>/<str:table_name>/", ExportPdfView.as_view(), name="export-pdf"),
    path("export/excel/<int:connection>/<str:table_name>/", ExportExcelView.as_view(), name="export-excel"),
    path("export/text/<int:connection>/<str:table_name>/", ExportTextView.as_view(), name="export-text"),
    path("import/csv/<int:connection>/", ImportCsvView.as_view(), name="import-csv"),

]
