from django.apps import AppConfig


class EmailsConfig(AppConfig):
    name = "wab.core.emails"
    verbose_name = "Emails"

    def ready(self):
        pass
