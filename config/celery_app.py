import os

from celery import Celery
from django.conf import settings
from datetime import timedelta

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("wab", include=["wab.core.notifications.tasks"])

app.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_TIMEZONE=settings.CELERY_TIMEZONE,
    CELERY_ENABLE_UTC=True,
    CELERYBEAT_SCHEDULE={
        'push_notification': {
            'task': 'wab.core.notifications.tasks.push_notification',
            'schedule': timedelta(seconds=30),
        }
    }
)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
