from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from django import forms
from .models import Receipt
import filetype

VALID_FILE_TYPES = ['application/pdf', 'image/jpeg']


def validate_file_type(file: UploadedFile):
    kind = filetype.guess(file)
    if kind is None or kind.mime not in VALID_FILE_TYPES:
        error = f"Invalid file type. File should be one of these types: {','.join(VALID_FILE_TYPES)}"
        raise ValidationError(error)


def validate_email(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError(
            (f"{value} is taken."),
            params={'value': value}
        )


class NewReceiptForm(forms.Form):
    # docs: https://docs.djangoproject.com/en/4.1/topics/forms/
    receipt_file = forms.FileField(
        label='Upload a receipt', widget=forms.FileInput(attrs={'class': "form-control"}), validators=[validate_file_type])


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True, validators=[validate_email])

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class EditReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = ['business_name', 'date', 'total']
