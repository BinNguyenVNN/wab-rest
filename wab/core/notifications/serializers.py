from wab.core.notifications.models import Channel, NotifyUser, Subscribe, Notifications
from rest_framework import serializers


class ChanelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ('name', 'type')


class NotifyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotifyUser
        fields = '__all__'


class NotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = '__all__'


class SubscribeSerializer(serializers.ModelSerializer):
    user__username = serializers.SerializerMethodField()
    channel__name = serializers.SerializerMethodField()
    channel__type = serializers.SerializerMethodField()

    def get_user__username(self, sub):
        return sub.user.username

    def get_channel__name(self, sub):
        return sub.channel.name

    def get_channel__type(self, sub):
        return sub.channel.type

    class Meta:
        model = Subscribe
        fields = ('user__username', 'channel__name', 'channel__type', 'app', 'active', 'active_date',
                  'contact')
