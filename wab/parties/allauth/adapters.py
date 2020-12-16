from typing import Any

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpRequest
from django.template.loader import render_to_string

from wab.core.emails.helpers import context_render_from_template

class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def render_mail(self, template_prefix, email, context):
        """
        Renders an e-mail to `email`.  `template_prefix` identifies the
        e-mail that is to be sent, e.g. "account/email/email_confirmation"
        """
        print(context)
        subjects = {
            'account/email/email_confirmation_signup': 'allauth_signup',
            'account/email/password_reset_key': 'allauth_reset',
        }
        mail_type = subjects[template_prefix]

        subject = render_to_string('{0}_subject.txt'.format(template_prefix),
                                   context)
        # remove superfluous line breaks
        subject = " ".join(subject.splitlines()).strip()
        subject = self.format_email_subject(subject)

        from_email = self.get_from_email()

        bodies = context_render_from_template(mail_type, context)

        msg = EmailMessage(subject,
                           bodies,
                           from_email,
                           [email])
        msg.content_subtype = 'html'  # Main content is now text/html
        return msg


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest, sociallogin: Any):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)
