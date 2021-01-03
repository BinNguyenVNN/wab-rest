from django.conf import settings
from pyfcm import FCMNotification

from wab.core.notifications.models import Subscribe
from wab.utils.db_manager import Singleton


class GFireBase:

    def __init__(self, channel):
        self.config = channel.config
        self.push_service = FCMNotification(api_key=settings.FCM_API_SERVER_KEY)

    def notify_single(self, message):
        # TODO: Add model for subscribe
        list_username = list(message.user.all().values_list("username", flat=True))
        subscriptions = Subscribe.objects.filter(
            user__username__in=list_username,
            channel_id=message.channel.id,
            active=True).values_list('contact', flat=True)

        list_contact = []
        for contacts in subscriptions:
            for contact in contacts:
                list_contact.append(contact)
        subscriptions = list(list_contact)
        valid_registration_ids = self.push_service.clean_registration_ids(subscriptions)
        image = message.data.get('image')
        click_url = message.data.get('url')

        result = self.push_service.notify_multiple_devices(registration_ids=valid_registration_ids,
                                                           message_title=message.title,
                                                           message_body=message.body,
                                                           extra_notification_kwargs={"image": image},
                                                           data_message=message.data,
                                                           click_action="FLUTTER_NOTIFICATION_CLICK",
                                                           content_available=True,
                                                           extra_kwargs={"mutable_content": True}
                                                           )
        return result

    def notify_broadcast(self, message):
        image = message.data.get('image')
        click_url = message.data.get('url')
        topic = message.data.get("topic")
        user_type = message.data.get("user_type") if message.data.get("user_type") else "unknown_user"
        channel = message.channel
        topic_channel = f"{channel.type}_{user_type}"
        result = self.push_service.notify_topic_subscribers(topic_name=topic_channel,
                                                            message_title=message.title,
                                                            message_body=message.body,
                                                            extra_notification_kwargs={"image": image},
                                                            data_message=message.data,
                                                            click_action="FLUTTER_NOTIFICATION_CLICK",
                                                            content_available=True,
                                                            extra_kwargs={"mutable_content": True})
        return result

    def subscribe_topic(self, channel, registration_ids):
        topic_channel = f"{channel.type}"
        registration_ids = list(registration_ids)
        result = self.push_service.subscribe_registration_ids_to_topic(registration_ids, topic_channel)
        return result

    def unsubscribe_topic(self, channel, registration_ids):
        topic_channel = f"{channel.type}"
        registration_ids = list(registration_ids)
        result = self.push_service.unsubscribe_registration_ids_from_topic(registration_ids, topic_channel)
        return result

    def validate_registration_id(self, token_id):
        subscriptions = list(token_id)
        print(subscriptions)
        valid_registration_ids = self.push_service.clean_registration_ids(subscriptions)
        print(valid_registration_ids)
        if len(valid_registration_ids) > 0:
            return True, valid_registration_ids
        return False, []


class FirebaseManager(object):
    __metaclass__ = Singleton
    fire_bases = {}

    def get_by_channel(self, channel):
        if channel.id in self.fire_bases.keys():
            return self.fire_bases[channel.id]
        else:
            firebase = GFireBase(channel)
            self.fire_bases[channel.id] = firebase
            return firebase
