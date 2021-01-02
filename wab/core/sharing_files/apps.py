from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SqlFunctionConfig(AppConfig):
    name = "wab.core.sharing_files"
    verbose_name = _("SharingFiles")

    def ready(self):
        try:
            import wab.core.sql_function.signals  # noqa F401
        except ImportError:
            pass
