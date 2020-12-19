from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SqlFunctionConfig(AppConfig):
    name = "wab.core.sql_function"
    verbose_name = _("SqlFunction")

    def ready(self):
        try:
            import wab.core.sql_function.signals  # noqa F401
        except ImportError:
            pass
