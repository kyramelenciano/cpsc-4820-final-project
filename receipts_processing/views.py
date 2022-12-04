import re
from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
import os
from . import filereader
import spacy
from spacy import displacy
from .models import Receipt
from .forms import NewReceiptForm
from django.contrib.auth.decorators import login_required


dirname = os.path.dirname(__file__)
model_path = os.path.join(dirname, "ner-models/model-best")
model = spacy.load(model_path)


def home(request):
    return render(request, 'receipts_processing/home.html')


@login_required
def receipts(request):
    receipts_list = Receipt.objects.filter(user=request.user)
    return render(request,  'receipts_processing/receipts.html', context={'receipts': receipts_list})


@login_required
def new(request):
    if request.method == 'GET':
        form = NewReceiptForm()
        return render(request, 'receipts_processing/index.html', {'form': form})
    elif request.method == 'POST':
        form = NewReceiptForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, 'receipts_processing/index.html', {'form': form})

        receipt_file = form.cleaned_data['receipt_file']
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
        new_receipt.user = request.user
        new_receipt.save()

        return redirect(f"/receipts/{new_receipt.id}")


@login_required
def receipt_details(request, id):
    receipt = get_object_or_404(Receipt, id=id, user=request.user)
    return render(request, "receipts_processing/receipt-details.html", {'receipt': receipt})


@login_required
def delete(request, id):
    receipt = get_object_or_404(Receipt, id=id, user=request.user)
    receipt.delete()
    return redirect('/receipts')


@login_required
def download(request, id):
    receipt = get_object_or_404(Receipt, id=id, user=request.user)
    path_to_file = os.path.realpath(receipt.file.name)
    response = FileResponse(open(path_to_file, 'rb'))
    response['Content-Disposition'] = 'attachment; filename=' + receipt.filename
    return response


@login_required
def view_file(request, id):
    receipt = get_object_or_404(Receipt, id=id, user=request.user)
    path_to_file = os.path.realpath(receipt.file.name)
    response = FileResponse(open(path_to_file, 'rb'))
    response['Content-Disposition'] = 'inline'
    return response


def parseAmountText(text):
    string_amount = re.sub(r"[$CADS\s]", "", text)
    if string_amount == "" or not string_amount.replace('.', '', 1).isnumeric():
        return None
    return float(string_amount)


def first(ls, filterFn):
    filteredList = list(filter(filterFn, ls))
    return filteredList[0] if len(
        filteredList) > 0 else None
