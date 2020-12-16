from django.db import migrations

from wab.core.emails.models import EmailTemplate


def update_site_forward(apps, schema_editor):
    """Auto create Email template"""
    EmailTemplate.objects.create(code="allauth_signup", content="\
        Hello from {{ current_site.name }}!\
        You're receiving this e-mail because user {{ user_display }} has given your e-mail address to register an account on {{ current_site.name }}.\
        To confirm this is correct, go to {{ activate_url }}\
        Thank you from {{ current_site.name }}!\
        {{ current_site.domain }}\
        ")
    EmailTemplate.objects.create(code="allauth_reset", content="\
        Hello from {{ current_site.name }}!\
        You're receiving this e-mail because you or someone else has requested a password for your user account.\
        It can be safely ignored if you did not request a password reset. Click the link below to reset your password.\
        {{ password_reset_url }}\
        In case you forgot, your username is {{ username }}.\
        Thank you for using {{ current_site.name }}!\
        {{ current_site.domain }}\
        ")
    EmailTemplate.objects.create(code="wab_invite", content="\
        Hello from {{ current_site.name }}!\
        You're receiving this e-mail because you have invite to {{ble}}.\
        Click the link below to create your account.\
        {{ invite_register_url }}\
        Thank you for using {{ current_site.name }}!\
        {{ current_site.domain }}\
        ")


def update_site_backward(apps, schema_editor):
    """Delete all Email template"""
    EmailTemplate.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [("emails", "0001_initial")]

    operations = [migrations.RunPython(update_site_forward, update_site_backward)]
