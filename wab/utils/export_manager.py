from __future__ import absolute_import

import logging
from datetime import datetime
from io import BytesIO, SEEK_SET
from wsgiref.util import FileWrapper

from django.core.files import File
from django.http import HttpResponse
from django.template.loader import select_template
from xhtml2pdf import pisa

from wab.utils.pdf import fetch_resources

logger = logging.getLogger(__name__)


class GeneratePdf(object):
    data = None
    collection_name = None
    columns = None

    def __init__(self, data, collection_name, columns):
        self.data = data
        self.collection_name = collection_name
        self.columns = columns

    def __get_pdf_filename(self):
        return '{name}_{date}.pdf'.format(
            name=str(self.collection_name),
            date=datetime.now().strftime("%d%m%Y-%H%M%S"),
        )

    @staticmethod
    def __generate(template, context, upload=True):
        html = template.render(context)
        pdf_file_object = BytesIO()
        pisa_status = pisa.pisaDocument(
            src=BytesIO(html.encode("UTF-8")),
            dest=pdf_file_object,
            encoding='UTF-8',
            link_callback=fetch_resources
        )

        if pisa_status.err:
            logger.error(
                'xhtml2pdf encountered exception during generation of pdf %s: %s',
                context['filename'],
                pisa_status.err
            )
            return
        return pdf_file_object

    # def __upload(self, pdf_file_object, location):
    #     pdf_file_object.seek(0, SEEK_SET)
    #     django_file = File(pdf_file_object)
    #     with transaction.atomic():
    #         self.pdf_file.save(filename, django_file, True)
    #         self.mark_as_clean()

    def generate_pdf(self, context):
        context['data'] = self.data
        context['columns'] = self.columns
        context['filename'] = self.__get_pdf_filename()
        context['table_name'] = self.collection_name
        pdf_file_object = self.__generate(template=select_template(['pdf/pdf_document.html']),
                                          context=context)
        pdf_file_object.seek(0, SEEK_SET)
        django_file = File(pdf_file_object)
        wrapper = FileWrapper(django_file)
        response = HttpResponse(wrapper, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=' + self.__get_pdf_filename()
        return response
        # self.__upload(self)
