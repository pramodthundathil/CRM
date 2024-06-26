# Generated by Django 3.1.1 on 2024-05-04 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Contacts', '0002_auto_20240504_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentcontact',
            name='collage',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='studentcontact',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='studentcontact',
            name='follow_up_started_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='studentcontact',
            name='study_streem',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
    ]
