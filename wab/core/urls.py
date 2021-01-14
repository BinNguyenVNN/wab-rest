from django.urls import include, path

from wab.core.export_database.views import ExportPdfView, ExportExcelView, ExportTextView
from wab.core.import_database.views import ImportCsvView
from wab.core.views import ListOperatorView, ListJoinView, ListRelationView, ListDataTypeView

urlpatterns = [
    path("users/", include("wab.core.users.urls")),
    path("", include("wab.core.custom_column.urls")),
    path("", include("wab.core.custom_column_fk.urls")),
    path("db-provider/", include("wab.core.db_provider.urls")),
    path("sql-function/", include("wab.core.sql_function.urls")),
    path("export/pdf/<int:connection>/<str:table_name>/", ExportPdfView.as_view(), name="export-pdf"),
    path("export/excel/<int:connection>/<str:table_name>/", ExportExcelView.as_view(), name="export-excel"),
    path("export/text/<int:connection>/<str:table_name>/", ExportTextView.as_view(), name="export-text"),
    path("import/csv/<int:connection>/<str:table_name>/", ImportCsvView.as_view(), name="import-csv"),
    path("notifications/", include("wab.core.notifications.urls")),
    path("sharing-files/", include("wab.core.sharing_files.urls")),
    path("list-operator/", ListOperatorView.as_view(), name='list-operator'),
    path("list-join/", ListJoinView.as_view(), name='list-operator'),
    path("list-relation/", ListRelationView.as_view(), name='list-relation'),
    path("list-data-type/", ListDataTypeView.as_view(), name='list-data-type'),
]
