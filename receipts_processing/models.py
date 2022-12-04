from django.db import models
from django.contrib.auth.models import User
# Create your models here


class Receipt(models.Model):
    class Meta:
        db_table = 'receipts'
    file = models.FileField(upload_to="uploaded-receipts", null=True)
    filename = models.CharField(max_length=100, null=True)
    type = models.CharField(max_length=100, null=True)
    business_name = models.CharField(max_length=100, null=True)
    date = models.CharField(max_length=50,  null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2,  null=True)
    text = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
