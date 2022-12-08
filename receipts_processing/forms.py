from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from django import forms
import filetype

VALID_FILE_TYPES = ['application/pdf', 'image/jpeg']


def validate_file_type(file: UploadedFile):
    kind = filetype.guess(file)
    if kind is None or kind.mime not in VALID_FILE_TYPES:
        error = f"Invalid file type. File should be one of these types: {','.join(VALID_FILE_TYPES)}"
        raise ValidationError(error)


class NewReceiptForm(forms.Form):
    # docs: https://docs.djangoproject.com/en/4.1/topics/forms/
    receipt_file = forms.FileField(
        label='Upload a receipt', widget=forms.FileInput(attrs={'class': "form-control"}), validators=[validate_file_type])
