from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from wab.utils.jsonb import JSONField

NOTIFY, POPUP = ("notify", "popup")

INIT, SENDING, SENT, READ, PENDING, REJECTED = (
    'init', 'sending', 'sent', 'read', 'pending', 'rejected'
)

EMAIL_CHANNEL, PUSH_NOTIFICATION = (
    'email', 'push_notification'
)

CHANNEL_TYPES = (
    (EMAIL_CHANNEL, _('Email channel')),
    (PUSH_NOTIFICATION, _('Push notification channel'))
)


class NotifyUser(models.Model):
    username = models.CharField(
        _('username'),
        max_length=150
    )
    date_update = models.DateTimeField(auto_now=True)
    added_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    def __str__(self):
        return str(self.username)

    class Meta:
        db_table = 'notify_user'


class Channel(models.Model):
    name = models.CharField(max_length=128, blank=True, null=True)
    type = models.CharField(max_length=64, choices=CHANNEL_TYPES, default=EMAIL_CHANNEL)
    description = models.TextField(blank=True)
    template = models.TextField(blank=True)
    config = JSONField(blank=True, null=True)
    active = models.BooleanField(blank=True, null=True, default=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'notify_channel'


class Subscribe(models.Model):
    user = models.ForeignKey(NotifyUser, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    active = models.BooleanField(blank=True, null=True)
    active_date = models.DateTimeField(blank=True, null=True)
    contact = ArrayField(models.CharField(max_length=200), blank=True, null=True, default=list)
    app = models.CharField(max_length=64, default="HAPPY")

    # contact: email, mobile, uuid

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'notify_subscribe'


CODE_STATUS_CHOICES = (
    (INIT, _('init')),
    (SENDING, _('sending')),
    (SENT, _('send')),
    (READ, _('read')),
    (PENDING, _('pending')),
    (REJECTED, _('rejected')),
)


class Notifications(models.Model):
    user = models.ManyToManyField(NotifyUser, blank=True, null=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=64, choices=CODE_STATUS_CHOICES, default=INIT)
    title = models.CharField(max_length=512, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    data = JSONField(blank=True, null=True)
    response = JSONField(blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        db_table = 'notifications'
