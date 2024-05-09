from django.db import models
from django.contrib.auth.models import User 

# Create your models here.

class CompanyProfile(models.Model):
    user = models.ManyToManyField(User)
    Company_Name = models.CharField(max_length=20,null=True, blank=True)
    Company_Profile_Description = models.CharField(max_length=255,null=True, blank=True)
    City = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    Company_Logo = models.FileField(upload_to="Company_logo",null=True, blank=True)





