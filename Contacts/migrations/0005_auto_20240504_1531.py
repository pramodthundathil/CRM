# Generated by Django 3.1.1 on 2024-05-04 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Contacts', '0004_auto_20240504_1223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentcontact',
            name='contact_number',
            field=models.IntegerField(),
        ),
    ]
