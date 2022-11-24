from borb.pdf.document.document import Document
from borb.pdf.pdf import PDF
from borb.toolkit.ocr.ocr_as_optional_content_group import OCRAsOptionalContentGroup
from borb.toolkit.text.simple_text_extraction import SimpleTextExtraction
from django.core.files.uploadedfile import UploadedFile
from numpy import asarray
from paddleocr import PaddleOCR
from PIL import Image
import filetype
import ftfy
import typing

ocr_model = PaddleOCR(lang='en', show_log=False)


def readFile(file: UploadedFile):
    kind = filetype.guess(file)
    if kind is None:
        raise Exception('Unknown file type')
    if kind.mime == 'application/pdf':
        return (kind.mime, getPdfText(file))
    elif kind.mime in ['image/jpeg']:
        return (kind.mime, getImgText(file))
    raise Exception('Unknown file type')


def getImgText(file: UploadedFile):
    lines = []
    result = ocr_model.ocr(asarray(Image.open(file)))
    res = result[0]
    for line in res:
        lines.append(line[1][0])
    return '\n'.join(lines)


def getPdfText(uploadedFile: UploadedFile):
    d: typing.Optional[Document] = None
    l: SimpleTextExtraction = SimpleTextExtraction()

    d = PDF.loads(uploadedFile.file, [l])

    assert d is not None

    invoiceText: str = ''
    page = 0
    reading = True
    while reading:
        pageText = l.get_text_for_page(page)
        invoiceText += pageText
        if pageText == '':
            reading = False
        page += 1
    return ftfy.fix_text(invoiceText)
