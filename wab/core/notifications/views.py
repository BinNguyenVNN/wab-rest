# Create your views here.
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from wab.core.notifications.firebasemanager import FirebaseManager
from wab.core.notifications.models import PUSH_NOTIFICATION, Channel, NotifyUser, Subscribe
from wab.core.notifications.serializers import SubscribeSerializer, NotificationsSerializer
from wab.core.notifications.services.notifications_service import NotificationsService
from wab.utils import responses, constant, token_authentication


class PushSingleNotificationsViews(CreateAPIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    serializer_class = NotificationsSerializer

    def post(self, request, **kwargs):
        data = request.data
        if data.get("username") is None:
            return responses.bad_request(data=None, message_code="USERNAME_INVALID")
        notify_service = NotificationsService()
        notify_service.process_push_single_notification(data=data)
        return responses.ok(data="Pushed single notifications!", method="post", entity_name="notifications")


class PushBroadcastNotificationsViews(CreateAPIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    serializer_class = NotificationsSerializer

    def post(self, request, **kwargs):
        data = request.data
        notify_service = NotificationsService()
        notify_service.process_push_broadcast_notification(data=data)
        return responses.ok(data="Pushed broadcast notifications", method="post", entity_name="notifications")


class RegisterTokenIdView(CreateAPIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    serializer_class = NotificationsSerializer

    def post(self, request, **kwargs):
        data = request.data
        username = data.get('username')
        channel = PUSH_NOTIFICATION
        app = "WAB"
        prev_reg_id = data.get('prev_reg_id')
        reg_id = data.get('reg_id')
        # validate channel requested
        if not Channel.objects.filter(type=channel).exists():
            return responses.bad_request(data=None, message_code="Channel is not existed!")
        else:
            channel = Channel.objects.filter(type=channel).first()
        user_notify = NotifyUser.objects.filter(username=username).first()
        if user_notify is None:
            # not existed, create new user
            user_notify = NotifyUser.objects.create(
                username=username
            )
        if prev_reg_id and prev_reg_id != "":
            subscribe = Subscribe.objects.filter(user=user_notify, app=app, channel_id=channel.id,
                                                 contact__contains=[prev_reg_id]).first()
            if not subscribe:
                return responses.bad_request(data=None, message_code="User subscription is invalid!")

            if channel.type == PUSH_NOTIFICATION:
                firebase_mgr = FirebaseManager()
                firebase = firebase_mgr.get_by_channel(channel)
                firebase.unsubscribe_topic(channel, [prev_reg_id])

                subscribe.contact.remove(prev_reg_id)
                subscribe.save()
        # check subscription
        if reg_id and reg_id != "":
            subscribe = Subscribe.objects.filter(user=user_notify, channel_id=channel.id, app=app).first()

            # Subscribe channel
            if not subscribe:
                subscribe = Subscribe.objects.create(
                    user=user_notify,
                    active=True,
                    channel_id=channel.id,
                    app=app
                )
            if channel.type == PUSH_NOTIFICATION:
                firebase_mgr = FirebaseManager()
                firebase = firebase_mgr.get_by_channel(channel)
                subscribe.contact.append(reg_id)
                is_valid, list_contact = firebase.validate_registration_id(subscribe.contact)
                if is_valid and reg_id in list_contact:
                    firebase.subscribe_topic(channel, [reg_id])
                    subscribe.contact = list_contact
                    subscribe.save()
                else:
                    return responses.bad_request(data=None, message_code="User token is invalid")

        return responses.ok(data=None, method=constant.POST, entity_name='notify')


class CheckRegisterTokenIdView(CreateAPIView):
    authentication_classes = [token_authentication.JWTAuthenticationBackend, ]
    serializer_class = NotificationsSerializer

    def post(self, request, **kwargs):
        data = request.data
        username = data.get('username')
        channel = PUSH_NOTIFICATION
        app = "WAB"
        # validate channel requested
        if not Channel.objects.filter(type=channel).exists():
            return responses.bad_request(None, "Channel is not existed!")
        else:
            channel = Channel.objects.filter(type=channel).first()

        user_notify = NotifyUser.objects.filter(username=username).first()
        if user_notify is None:
            user_notify = NotifyUser.objects.create(
                username=username
            )

        # check subscription
        if not Subscribe.objects.filter(user=user_notify, channel_id=channel.id, app=app).exists():
            return responses.ok(data={"is_subscribe": False}, method=constant.POST, entity_name='notify')

        subscription = Subscribe.objects.filter(user=user_notify, channel_id=channel.id, app=app).first()
        serializer = SubscribeSerializer(subscription)
        resp = serializer.data
        resp["is_subscribe"] = True
        return responses.ok(data=resp, method=constant.POST, entity_name='notify')
