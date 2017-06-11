import codecs

from dbHandler import insert_into_db
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams

from io import StringIO

def pdf_to_text(pdfname):

    # PDFMiner boilerplate
    resourceManager = PDFResourceManager()
    sio = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(resourceManager, sio, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(resourceManager, device)
    # Extract text
    fp = open(pdfname, 'rb')
    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
    fp.close()
    # Get text from StringIO
    text = sio.getvalue()
    # Cleanup
    device.close()
    sio.close()
    return text

def text_writer(document_list):

    for doc in document_list:
        text_stream = pdf_to_text(doc)
        file = codecs.open(str(doc) + ".txt", 'w', 'utf-8')
        file.write(text_stream)
        file.close()

def json_list_creator(document_list):

    text_document_list = list()
    for doc in document_list:
        text_stream = pdf_to_text(doc)
        document = {
            "doc_name": str(doc),
            "doc_content": text_stream
        }
        text_document_list.append(document)
    return text_document_list

# json_list = json_list_creator(document_list)
# insert_into_db(json_list)

# text_writer(document_list)