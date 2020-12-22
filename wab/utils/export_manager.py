from __future__ import absolute_import

import logging
from datetime import datetime
from io import BytesIO, SEEK_SET

from django.template.loader import select_template
from xhtml2pdf import pisa

from silver.api.azure_upload_services import function_upload
from silver.models import Transaction, BillingDocumentBase, Invoice, DocumentEntry
from silver.utils.pdf import fetch_resources

logger = logging.getLogger(__name__)


class GeneratePDFOfTransaction(object):
    db = None
    collection_name = None

    def __init__(self, db, collection_name):
        self.db = db
        self.collection_name = collection_name

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

    def __upload(self, pdf_file_object, location):
        # the PDF's upload_path attribute needs to be set before calling this method
        # pdf_file_object.seek(0, SEEK_SET)
        # url = function_upload(image=pdf_file_object, location=location, content_type='application/pdf',
        #                       name=self.__get_pdf_filename())
        # self.transaction.pdf = url
        # self.transaction.save()
        # return self.transaction
        pass

    def generate_pdf(self, context):
        context['db'] = self.db
        context['collection_name'] = self.collection_name
        context['filename'] = self.__get_pdf_filename()
        pdf_file_object = self.__generate(template=select_template(['pdf/pdf_document.html']),
                                          context=context)
        self.__upload(self)
        return None
