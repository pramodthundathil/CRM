# Generated by Django 3.1.1 on 2024-04-22 05:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Home', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companyprofile',
            name='user',
        ),
        migrations.AddField(
            model_name='companyprofile',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
