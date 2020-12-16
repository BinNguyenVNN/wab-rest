from django.template import Context, Template

from wab.core.emails.models import EmailTemplate


def context_render_from_template(code, context):
    try:
        content = EmailTemplate.objects.get(code=code).content
        content_template = Template(content)
        return content_template.render(Context(context))
    except EmailTemplate.DoesNotExist:
        return None
