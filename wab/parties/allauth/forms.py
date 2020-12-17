from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template
from django.utils.translation import ugettext as _
from django.contrib.auth.tokens import default_token_generator
from wab.core.users.models import User, KeyModel


class ConfirmEmailForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)

        super(forms.Form, self).__init__(*args, **kwargs)


class RequestConfirmEmailForm(forms.Form):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)

        super(forms.Form, self).__init__(*args, **kwargs)

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            if not email:
                error_msg = _('Email not empty or not valid')
                raise forms.ValidationError(error_msg)
            else:
                user = User.objects.filter(email=email).first()
                if user:
                    token = default_token_generator.make_token(user)
                    KeyModel.objects.filter(user=user).delete()
                    KeyModel.objects.create(key=token, user=user)
                    context = {
                        'username': user.username,
                        'activate_url': settings.WAB_API + 'oauth/registration/confirm-email/' + token + '/',
                        'fe_url': settings.WAB_FE
                    }
                    html_message = get_template("account/wab/email_register.html").render(context)
                    send_mail(settings.EMAIL_SUBJECT_PREFIX + ' Please Confirm Your E-mail Address', None,
                              settings.DEFAULT_FROM_EMAIL, [email], html_message=html_message)
                else:
                    error_msg = _('Email not register')
                    raise forms.ValidationError(error_msg)
