# Generated by Django 5.0.6 on 2025-04-29 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoiceitem',
            name='quantity',
        ),
        migrations.AlterField(
            model_name='invoiceitem',
            name='product',
            field=models.CharField(max_length=1000),
        ),
    ]
