from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .drive import upload_file
# Create your models here


class Receipt(models.Model):
    # docs: https://docs.djangoproject.com/en/4.1/ref/models/options/
    class Meta:
        db_table = 'receipts'

    # docs: https://docs.djangoproject.com/en/4.1/ref/models/fields/
    file = models.FileField(upload_to="uploaded-receipts", null=True)
    filename = models.CharField(max_length=100, null=True)
    type = models.CharField(max_length=100, null=True)
    business_name = models.CharField(max_length=100, null=True)
    date = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2,  null=True)
    text = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


@receiver(post_save, sender=Receipt)
def upload_receipt_to_drive(sender, instance, **kwargs):
    # docs: https://docs.djangoproject.com/en/4.1/ref/signals/#post-save
    file_data = {
        'path': instance.file.path,
        'name': instance.filename,
        'mimetype': instance.type
    }
    upload_file(instance.user.id, file_data)
