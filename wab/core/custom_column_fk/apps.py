from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CustomColumnFK(AppConfig):
    name = "wab.core.custom_column_fk"
    verbose_name = _("CustomColumnFK")

    def ready(self):
        try:
            import wab.core.custom_column.signals  # noqa F401
        except ImportError:
            pass
