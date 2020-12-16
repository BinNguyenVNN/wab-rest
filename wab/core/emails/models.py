from django.db.models import BooleanField, CharField, TextField

from wab.core.components.models import BaseModel


class EmailTemplate(BaseModel):
    code = CharField("Specific code for core app", max_length=50, blank=True, null=True, editable=False, unique=True)
    is_protected = BooleanField("Is protected", default=False)
    content = TextField("Html content")
