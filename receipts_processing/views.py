import re
from django.http import HttpResponse
from django.shortcuts import render, redirect
import os
from . import filereader
import spacy
from spacy import displacy
from .models import Receipt

dirname = os.path.dirname(__file__)
model_path = os.path.join(dirname, "ner-models/model-best")
model = spacy.load(model_path)


def home(request):
    return render(request, 'receipts_processing/home.html')


def receipts(request):
    receipts_list = Receipt.objects.all()
    return render(request,  'receipts_processing/receipts.html', context={'receipts': receipts_list})


def index(request):
    if request.method == 'GET':
        return render(request, 'receipts_processing/index.html')
    elif request.method == 'POST':
        receipt_file = request.FILES['receipt']
        try:
            type, text = filereader.readFile(receipt_file)
            doc = model(text)
            ents = [{'text': ent.text, 'label': ent.label_}
                    for ent in doc.ents]
            businessNameEnt = first(
                ents, lambda e: e['label'] == 'ORG')

            dateEnt = first(
                ents, lambda e: e['label'] == 'DATE')
            moneyEnts = list(filter(lambda e: e['label'] == 'MONEY', ents))
            parsedMoneyEnts = [amount for amount in map(
                lambda e: parseAmountText(e['text']), moneyEnts) if amount is not None]

            new_receipt = Receipt()
            new_receipt.file = receipt_file
            new_receipt.filename = receipt_file.name
            new_receipt.type = type
            new_receipt.business_name = businessNameEnt['text'] if businessNameEnt else receipt_file.name
            new_receipt.date = dateEnt['text'] if dateEnt else None
            new_receipt.total = max(parsedMoneyEnts) if len(
                parsedMoneyEnts) > 0 else None
            new_receipt.text = text
            new_receipt.save()

        except BaseException as e:
            print(e)

        return redirect('/receipts')


def parseAmountText(text) -> float | None:
    string_amount = re.sub(r"[$CADS\s]", "", text)
    if string_amount == "" or not string_amount.replace('.', '', 1).isnumeric():
        return None
    return float(string_amount)


def first(ls, filterFn):
    filteredList = list(filter(filterFn, ls))
    return filteredList[0] if len(
        filteredList) > 0 else None
