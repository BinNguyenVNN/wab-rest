from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from wab.parties.allauth.views import AccountRegisterView, AccountLoginView, ConfirmEmailView, \
    confirm_email_done, confirm_email_expired, RequestConfirmEmailView, request_email_done, ResetPasswordRequestView, \
    password_rest_complete, SetPasswordView

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Web Application Base",
        contact=openapi.Contact(email="support@risotech.vn"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
                  path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                  path('redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
                  # Django Admin, use {% url 'admin:index' %}
                  path(settings.ADMIN_URL, admin.site.urls),
                  # AllAuth
                  # path('rest-auth/', include('dj_rest_auth.urls')),
                  # path("accounts/", include("allauth.urls")),
                  # DRF auth
                  # path("oauth/", include("rest_auth.urls")),
                  # path("oauth/registration/", include("rest_auth.registration.urls")),
                  path("oauth/login/", AccountLoginView.as_view(), name="login_view"),
                  path("oauth/registration/", AccountRegisterView.as_view(), name="create_view"),
                  # path("oauth/registration/confirm-email/", confirm_view,
                  #      name="confirm_view"),
                  path("oauth/registration/confirm-email/<str:key>/", ConfirmEmailView.as_view(),
                       name="confirm_email_view"),
                  path("oauth/registration/confirm/done/", confirm_email_done,
                       name="confirm_email_done"),
                  path("oauth/registration/confirm/expired/", confirm_email_expired,
                       name="confirm_email_expired"),
                  path("oauth/registration/confirm/request/", RequestConfirmEmailView.as_view(),
                       name="confirm_email_request"),
                  path("oauth/registration/request/done/", request_email_done,
                       name="request_email_done"),
                  path("accounts/reset-password/", ResetPasswordRequestView.as_view(),
                       name="request_reset_password_view"),
                  path("accounts/reset-password/confirm/<str:key>/", SetPasswordView.as_view(),
                       name="password_reset_confirm"),
                  path("accounts/reset-password/done/", password_rest_complete,
                       name="password_rest_done"),
                  # Core
                  path("core/", include("wab.core.urls")),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
