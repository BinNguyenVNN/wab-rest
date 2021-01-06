from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from wab.core.users.api.views import UserViewSet, UserUpdateProfileView

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("", UserViewSet)

app_name = "users"
urlpatterns = [
                  path("profile/", UserUpdateProfileView.as_view(), name='update-profile')
              ] + router.urls
