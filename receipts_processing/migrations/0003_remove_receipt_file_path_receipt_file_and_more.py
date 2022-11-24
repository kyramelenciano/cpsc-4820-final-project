# Generated by Django 4.1.3 on 2022-11-24 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("receipts_processing", "0002_rename_filepath_receipt_file_path_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="receipt",
            name="file_path",
        ),
        migrations.AddField(
            model_name="receipt",
            name="file",
            field=models.FileField(null=True, upload_to="uploaded-receipts"),
        )
    ]
