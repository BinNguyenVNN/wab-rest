from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DbProviderConfig(AppConfig):
    name = "wab.core.db_provider"
    verbose_name = _("DbProvider")

    def ready(self):
        try:
            import wab.core.db_provider.signals  # noqa F401
        except ImportError:
            pass
