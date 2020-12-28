from config.celery_app import app


@app.task
def push_notification(message_id=None):
    from wab.core.notifications.models import Notifications, PUSH_NOTIFICATION, INIT
    from wab.core.notifications.services.notifications_service import NotificationsService

    notify_service = NotificationsService()

    if message_id is None:
        messages = Notifications.objects.filter(status__in=[INIT], channel__type=PUSH_NOTIFICATION)
        for msg in messages:
            notify_service.process_push_notification_firebase(msg)

    elif Notifications.objects.filter(id=message_id, channel__type=PUSH_NOTIFICATION).exists():
        print("PUSH_NOTIFICATION %s" % message_id)
        msg = Notifications.objects.get(id=message_id)
        notify_service.process_push_notification_firebase(msg)
