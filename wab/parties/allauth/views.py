from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import render
from django.template.loader import get_template
from django.views.generic.edit import FormView
from rest_framework.generics import CreateAPIView
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from wab.core.users.models import User, KeyModel
from wab.parties.allauth.forms import ConfirmEmailForm, RequestConfirmEmailForm, PasswordSetFormExt
from wab.parties.allauth.serializers import RegisterUserSerializer, LoginUserSerializer, ResetPasswordRequestSerializer
from wab.utils import responses, constant


class LoginServices(object):
    serializer_class = None
    request = None

    def __init__(self, serializer_class, request):
        self.serializer_class = serializer_class
        self.request = request

    def login(self):
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid(raise_exception=True):
            return responses.ok(data=serializer.validate(self.request.data), method=constant.POST, entity_name='users')


class AccountLoginView(CreateAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = LoginUserSerializer

    def post(self, request):
        login_services = LoginServices(serializer_class=self.serializer_class, request=request)
        return login_services.login()


class AccountRegisterView(CreateAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = RegisterUserSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        password1 = data.get('password1')
        password2 = data.get('password2')
        username = data.get('username')
        email = data.get('email')
        user = User.objects.filter(Q(username=username) | Q(email=email)).first()
        if user is None:
            if password1 == password2:
                # user_create = {
                #     'username': username,
                #     'email': email,
                #     'password': make_password(password1)
                # }
                serializer = self.get_serializer(data=data)
                if serializer.is_valid(raise_exception=True):
                    # user = serializer.save()
                    user = User.objects.create(username=username, email=email, password=make_password(password1))
                    user.is_active = False
                    user.save()
                    current_site = get_current_site(self.request)
                    token = default_token_generator.make_token(user)
                    context = {
                        'username': username,
                        'activate_url': settings.WAB_API + 'oauth/registration/confirm-email/' + token + '/',
                        'fe_url': settings.WAB_FE
                    }
                    KeyModel.objects.create(key=token, user=user)
                    html_message = get_template("account/wab/email_register.html").render(context)
                    send_mail(settings.EMAIL_SUBJECT_PREFIX + ' Please Confirm Your E-mail Address', None,
                              settings.DEFAULT_FROM_EMAIL, [email], html_message=html_message)
                    return responses.ok(data='Register success', method=constant.POST, entity_name='users')
            else:
                return responses.bad_request(data='Password does not match', message_code='PASSWORD_NOT_SAME')
        else:
            return responses.bad_request(data='User is existed', message_code='USER_EXISTED')


class ConfirmEmailView(FormView):
    """
    (2.1 and 2.2) Credential requestor and acceptor.

    This view operates as a credential requestor when a GET request
    is received, and a credential acceptor for POST requests.
    """
    authentication_classes = ()
    template_name = 'account/wab/email_confirm_form.html'
    form_class = ConfirmEmailForm

    def get_form_kwargs(self):
        key = self.kwargs['key']
        user = self.check(self.request, key)
        self.request.user = user
        kwargs = super(ConfirmEmailView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def check(self, request, key=None, format=None):
        assert key is not None  # checked by URLconf
        user = None
        try:
            if key:
                key_user = KeyModel.objects.filter(key=key).first()
                if key_user:
                    user = key_user.user
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            return None

        if user is not None and default_token_generator.check_token(user, key):
            return user
        return None

    def get(self, request, *args, **kwargs):
        user = self.check(self.request, self.kwargs['key'])
        context = {}
        if user:
            context = {
                'key': self.kwargs['key'],
                'username': user.username,
                'email': user.email,
                'url': settings.WAB_API
            }
        return super(ConfirmEmailView, self).render_to_response(context)

    def form_valid(self, form):
        if self.request.user:
            user = self.request.user
            user.is_active = True
            user.save()
            KeyModel.objects.filter(user=user).delete()
            return HttpResponseRedirect(settings.WAB_API + 'oauth/registration/confirm/done/')
        return HttpResponseRedirect(settings.WAB_API + 'oauth/registration/confirm/expired/',
                                    {'link': settings.WAB_API + 'oauth/registration/confirm-email/request/'})


class RequestConfirmEmailView(FormView):
    """
    (2.1 and 2.2) Credential requestor and acceptor.

    This view operates as a credential requestor when a GET request
    is received, and a credential acceptor for POST requests.
    """
    authentication_classes = ()
    template_name = 'account/wab/email_confirm_request_form.html'
    form_class = RequestConfirmEmailForm

    def get_form_kwargs(self):
        kwargs = super(RequestConfirmEmailView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def check(self, request, email=None, format=None):
        assert email is not None  # checked by URLconf
        user = None
        try:
            if email:
                user = User.objects.filter(email=email).first()
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            return None

        if user is not None:
            return user
        return None

    def get(self, request, *args, **kwargs):
        context = {}
        return super(RequestConfirmEmailView, self).render_to_response(context)

    def form_valid(self, form):
        return HttpResponseRedirect(settings.WAB_API + 'oauth/registration/request/done/')


def confirm_email_done(request):
    url_dashboard = settings.WAB_FE
    return render(request, 'account/wab/email_confirm_done_form.html', {'url_dashboard': url_dashboard})


def confirm_email_expired(request):
    link = settings.WAB_API + 'oauth/registration/confirm/request/'
    return render(request, 'account/wab/email_confirm_expired_form.html', {'link': link})


def request_email_done(request):
    return render(request, 'account/wab/email_confirm_request_done_form.html', {})


class ResetPasswordRequestView(CreateAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', None)
        if email:
            user = User.objects.filter(email=email).first()
            if user:
                token = default_token_generator.make_token(user)
                context = {
                    'username': user.username,
                    'activate_url': settings.WAB_API + 'accounts/reset-password/confirm/' + token + '/'
                }
                KeyModel.objects.filter(user=user).delete()
                KeyModel.objects.create(key=token, user=user)
                html_message = get_template("account/wab/email_reset_password.html").render(context)
                send_mail(settings.EMAIL_SUBJECT_PREFIX + ' Reset password', None,
                          settings.DEFAULT_FROM_EMAIL, [email], html_message=html_message)
                return responses.ok(data='Reset success', method=constant.POST, entity_name='users')
            else:
                return responses.bad_request(data='User not found', message_code='USER_NOT_FOUND')
        else:
            return responses.bad_request(data='Email invalid', message_code='EMAIL_INVALID')


class SetPasswordView(FormView):
    """
    (2.1 and 2.2) Credential requestor and acceptor.

    This view operates as a credential requestor when a GET request
    is received, and a credential acceptor for POST requests.
    """
    authentication_classes = ()
    template_name = 'account/wab/password_reset_confirm_form.html'
    form_class = PasswordSetFormExt

    def get_form_kwargs(self):
        key = self.kwargs['key']
        user = self.check(self.request, key)
        self.request.user = user
        kwargs = super(SetPasswordView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def check(self, request, key=None, format=None):
        assert key is not None  # checked by URLconf
        user = None
        try:
            if key:
                key_user = KeyModel.objects.filter(key=key).first()
                if key_user:
                    user = key_user.user
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            return None

        if user is not None and default_token_generator.check_token(user, key):
            return user
        return None

    def get(self, request, *args, **kwargs):
        context = super(SetPasswordView, self).get_context_data()
        return super(SetPasswordView, self).render_to_response(context)

    def form_valid(self, form):
        return HttpResponseRedirect(settings.WAB_API + 'accounts/reset-password/done/')


def password_rest_complete(request):
    url_dashboard = settings.WAB_FE
    return render(request, 'account/wab/password_reset_done_form.html', {'url_dashboard': url_dashboard})
