import json

from wab.core.notifications.models import PUSH_NOTIFICATION, NOTIFY, POPUP


class NotificationsService(object):
    mqtt = None

    def __init__(self):
        # self.mqtt = MQTTServices().client
        pass

    def test_process_push_notification(self):
        payload_single = {
            "channel": PUSH_NOTIFICATION,
            "title": "Test Push Notifications to Single User",
            "body": "Body of Test Push Notifications to Single User",
            "data": {
                "username": "testabc",
                "notification_type": NOTIFY
            }
        }
        payload_broadcast = {
            "channel": PUSH_NOTIFICATION,
            "title": "Test Push Notifications to Single User",
            "body": "Body of Test Push Notifications to Single User",
            "data": {
                "notification_type": POPUP
            }
        }

        # self.process_push_single_notification(data=payload_single)
        # self.process_push_broadcast_notification(data=payload_broadcast)

    def process_push_single_notification(self, data: dict):
        from wab.core.notifications.topic import Topic
        json_data = data.get("data", {})
        json_data["topic"] = Topic.PUSH_SINGLE_NOTIFICATION
        json_data["username"] = data.get("username")
        payload = {
            "channel": PUSH_NOTIFICATION,
            "username": data.get("username"),
            "title": data.get("title"),
            "body": data.get("body"),
            "data": json_data
        }
        self.insert_notifications(payload=payload, topic=Topic.PUSH_SINGLE_NOTIFICATION)
        return True

    def process_push_broadcast_notification(self, data: dict):
        from wab.core.notifications.topic import Topic
        json_data = data.get("data", {})
        json_data["topic"] = Topic.PUSH_BROADCAST_NOTIFICATION
        payload = {
            "channel": PUSH_NOTIFICATION,
            "title": data.get("title"),
            "body": data.get("body"),
            "data": json_data
        }
        self.insert_notifications(payload=payload, topic=Topic.PUSH_BROADCAST_NOTIFICATION)
        return True

    def insert_notifications(self, topic: str, payload: dict):
        from wab.core.notifications.models import Channel, NotifyUser, Notifications, INIT, PUSH_NOTIFICATION
        from wab.core.notifications.topic import Topic

        data = payload.get("data")
        # Save DB
        channel = Channel.objects.filter(type=PUSH_NOTIFICATION).first()
        if not channel:
            print(f"Can't find Channel")
            return False
        if topic == Topic.PUSH_SINGLE_NOTIFICATION:
            username = data.get("username")
            if not username:
                print(f"Can't find User")
                return False

            list_user_notify = []
            if type(username) is str:
                if username == "":
                    print(f"Invalid value username")
                    return False
                # 1 user
                user_notify, _ = NotifyUser.objects.get_or_create(
                    username=username,
                )
                list_user_notify.append(user_notify)
            elif type(username) is list:
                if len(username) == 0:
                    print(f"Invalid value username")
                    return False
                # group user
                for u in username:
                    user_notify, _ = NotifyUser.objects.get_or_create(
                        username=u,
                    )
                    list_user_notify.append(user_notify)

            else:
                print(f"Type username is valid, must be str or list")
                return False

            notify = Notifications.objects.create(
                channel_id=channel.id,
                status=INIT,
                title=payload.get("title"),
                body=payload.get("body"),
                data=data,
            )
            notify.user = list_user_notify
            notify.save()

        elif topic == Topic.PUSH_BROADCAST_NOTIFICATION:
            Notifications.objects.create(
                channel_id=channel.id,
                status=INIT,
                title=payload.get("title"),
                body=payload.get("body"),
                data=data,
            )

        self.push_notification_firebase()

        return True

    def process_push_notification_firebase(self, msg):
        from wab.core.notifications.firebasemanager import FirebaseManager
        from wab.core.notifications.models import PENDING, SENT
        from wab.core.notifications.topic import Topic
        response = None
        try:
            firebase_mgr = FirebaseManager()
            firebase = firebase_mgr.get_by_channel(msg.channel)
            data = msg.data
            topic = data.get("topic")
            if topic == Topic.PUSH_BROADCAST_NOTIFICATION:
                response = firebase.notify_broadcast(msg)
            else:
                response = firebase.notify_single(msg)
            msg.status = SENT
            msg.response = response
            msg.save()
        except Exception as ex:
            print(str(ex))
            msg.status = PENDING
            msg.response = response if response else {"error": str(ex)}
            msg.save()
            pass

    def push_notification_firebase(self, message_id=None):
        from wab.core.notifications.models import Notifications, PUSH_NOTIFICATION, INIT
        if message_id is None:
            messages = Notifications.objects.filter(status__in=[INIT], channel__type=PUSH_NOTIFICATION)
            for msg in messages:
                self.process_push_notification_firebase(msg)

        elif Notifications.objects.filter(id=message_id, channel__type=PUSH_NOTIFICATION).exists():
            print("PUSH_NOTIFICATION %s" % message_id)
            msg = Notifications.objects.get(id=message_id)
            self.process_push_notification_firebase(msg)
