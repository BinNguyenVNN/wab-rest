from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Default user for Web Application Base."""

    #: First and last name do not cover name patterns around the globe
    name = models.CharField(_("Name of User"), blank=True, max_length=255)

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


class KeyModel(models.Model):
    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    user = models.OneToOneField(User, default=True, null=True, related_name='user_token',
                                on_delete=models.CASCADE)
    created = models.DateTimeField(_("Created"), auto_now_add=True)
