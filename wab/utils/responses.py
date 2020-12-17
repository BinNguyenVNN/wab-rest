from django.conf import settings
from django.utils.translation import activate
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.response import Response


def ok(data, method='get', entity_name=''):
    msg = 'wab.' + entity_name + '.updated'
    if method == 'put':
        msg = 'wab.' + entity_name + '.updated'
    elif method == 'post':
        msg = 'wab.' + entity_name + '.created'
    elif method == 'delete':
        msg = 'wab.' + entity_name + '.deleted'
    elif method == 'get':
        return Response(data=data, status=status.HTTP_200_OK, headers={})
    headers = {
        'X-wabapp-alert': msg
    }
    return Response(data=data, status=status.HTTP_200_OK, headers=headers)


def paging(data, total_count, method='get', entity_name=''):
    msg = 'wab.' + entity_name + '.updated'
    if method == 'put':
        msg = 'wab.' + entity_name + '.updated'
    elif method == 'post':
        msg = 'wab.' + entity_name + '.created'
    elif method == 'delete':
        msg = 'wab.' + entity_name + '.deleted'
    if method == 'get':
        headers = {
            'X-wabapp-total-count': total_count
        }
    else:
        headers = {
            'X-wabapp-alert': msg,
            'X-wabapp-total-count': total_count
        }
    return Response(data=data, status=status.HTTP_200_OK, headers=headers)


def not_found(data, message_code=None, message_system=None):
    activate(settings.LANGUAGE_CODE)
    if message_code is not None:
        message = _(message_code)
    else:
        message = None
    headers = {
        'X-wabapp-error': message_code,
        'X-wabapp-params': message
    }
    if message_system is not None:
        print(message_system)
    return Response(data=data, status=status.HTTP_404_NOT_FOUND, headers=headers)


def bad_request(data, message_code=None):
    activate(settings.LANGUAGE_CODE)
    message = _(message_code)
    headers = {
        'X-wabapp-error': message_code,
        'X-wabapp-params': message,
    }
    return Response(data=data, status=status.HTTP_400_BAD_REQUEST, headers=headers)


def service_unavailable(message='Service Unavailable'):
    headers = {
        'X-wabapp-error': 'SYSTEM_503',
        'X-wabapp-params': message,
    }
    return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE, headers=headers)


def authentication_failed(message='Authentication failed'):
    headers = {
        'X-wabapp-error': 'SYSTEM_401',
        'X-wabapp-params': message,
    }
    return Response(message, status=status.HTTP_401_UNAUTHORIZED, headers=headers)
