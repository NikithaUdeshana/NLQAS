import codecs
import os

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams

from io import StringIO

def pdf_to_text(pdfname):

    resourceManager = PDFResourceManager()
    stringio = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(resourceManager, stringio, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(resourceManager, device)

    fp = open("test files/" + pdfname, 'rb')
    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
    fp.close()

    text = stringio.getvalue()

    device.close()
    stringio.close()
    return text

def text_writer(document_list):

    for doc in document_list:
        text_stream = pdf_to_text(doc)
        file = codecs.open(str(doc) + ".txt", 'w', 'utf-8')
        file.write(text_stream)
        file.close()

def json_doc_creator(doc):
    text_stream = pdf_to_text(doc)
    # doc_name = str(os.path.splitext(doc)[0])
    document = {
        "doc_name": str(doc),
        "doc_content": text_stream
    }
    return document