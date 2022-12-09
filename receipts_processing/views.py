from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
import os
from .models import Receipt
from .forms import NewReceiptForm
from django.contrib.auth.decorators import login_required
from .receipts import get_receipt_info_from_file


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
        return render(request, 'receipts_processing/new-receipt.html', {'form': form})
    elif request.method == 'POST':

        form = NewReceiptForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, 'receipts_processing/new-receipt.html', {'form': form})

        receipt_file = form.cleaned_data['receipt_file']
        receipt_info = get_receipt_info_from_file(receipt_file)

        new_receipt = Receipt()
        new_receipt.file = receipt_file
        new_receipt.filename = receipt_file.name
        new_receipt.type = receipt_info['type']
        new_receipt.business_name = receipt_info['business_name']
        new_receipt.date = receipt_info['date']
        new_receipt.total = receipt_info['total']
        new_receipt.text = receipt_info['text']
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
