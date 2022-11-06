import re
from django.http import HttpResponse
from django.shortcuts import render
import os
from . import filereader
import spacy
from spacy import displacy

dirname = os.path.dirname(__file__)
model_path = os.path.join(dirname, "ner-models/model-best")
model = spacy.load(model_path)


def index(request):
    if request.method == 'GET':
        return render(request, 'receipts_processing/index.html')
    elif request.method == 'POST':
        receipt = request.FILES['receipt']
        try:
            text = filereader.readFile(receipt)
            doc = model(text)
            html = displacy.render(doc, style="ent")
            context = {
                'success': True,
                'filename': receipt.name,
                'results': html
            }
        except BaseException as e:
            context = {
                'error_message': str(e)
            }

        return render(request, 'receipts_processing/results.html', context)
