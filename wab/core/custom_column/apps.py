from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CustomColumnTypeConfig(AppConfig):
    name = "wab.core.custom_column"
    verbose_name = _("CustomColumnType")

    def ready(self):
        try:
            import wab.core.custom_column.signals  # noqa F401
        except ImportError:
            pass
