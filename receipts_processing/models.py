from django.db import models

# Create your models here


class Receipt(models.Model):
    class Meta:
        db_table = 'receipts'
    file_path = models.CharField(max_length=100)
    business_name = models.CharField(max_length=100, null=True)
    date = models.CharField(max_length=50,  null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2,  null=True)
    text = models.TextField(null=True)
