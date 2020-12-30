from django.urls import path

from wab.core.notifications.views import PushSingleNotificationsViews, PushBroadcastNotificationsViews, \
    RegisterTokenIdView, CheckRegisterTokenIdView

urlpatterns = [
    path('single/push', PushSingleNotificationsViews.as_view(), name='PushSingleNotificationsViews'),
    path('broadcast', PushBroadcastNotificationsViews.as_view(), name='PushBroadcastNotificationsViews'),
    path('register-token', RegisterTokenIdView.as_view(), name='RegisterTokenIdView'),
    path('register-token/check', CheckRegisterTokenIdView.as_view(), name='CheckRegisterTokenIdView'),
]
