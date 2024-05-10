from django.db import models
from django.contrib.auth.models import User

class StudentContact(models.Model):
    name = models.CharField(max_length=200)
    contact_number = models.IntegerField()
    email = models.EmailField(null=True, blank=True,default="")
    study_streem = models.CharField(max_length=20, null= True, blank=True,default="")
    collage = models.CharField(max_length=20, null= True, blank=True,default="")
    DOB = models.DateField(null=True, blank=True)
    added_date = models.DateTimeField(auto_now_add=True)
    follow_up_started_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    last_follow_up = models.DateField(auto_now_add=False, null=True, blank=True)
    number_follow_up = models.PositiveBigIntegerField(default=0)
    options = (("Not Called","Not Called"),("RNR","RNR"),("Not Taken","Not Taken"),("Not intrested","Not intrested"),("Line Busy","Line Busy"),("Intrested","Intrested"),("Sligtly Intrested","Sligtly Intrested"),("Call Back","Call Back"))
    follow_up_status = models.CharField(max_length=20,default="Not Called",choices=options)
    last_status = models.TextField(max_length=1000,default="Fresh Data",null=True, blank=True)
    next_follow_up = models.DateField(auto_now_add=False, null=True, blank=True)
    options1 = (("Warm Lead","Warm Lead"),("Hot Lead", "Hot Lead"),("Pending","Pending"),("Converted","Converted"),("Rejected","Rejected"))
    lead_status = models.CharField(default="Normal",choices = options1, max_length=255,null=True, blank=True)
    active = models.BooleanField(default=True)
    lead_follow_up = models.ForeignKey(User, on_delete=models.DO_NOTHING, null= True, blank=True)

    def __str__(self):
        return str(self.name)


class LeadCallStatus(models.Model):
    contact = models.ForeignKey(StudentContact, on_delete=models.CASCADE)
    date_of_follow_up = models.DateTimeField(auto_now_add=True)
    options = (("RNA","RNA"),("Not Taken","Not Taken"),("Not intrested","Not intrested"),("Line Busy","Line Busy"),("Intrested","Intrested"),("Sligtly Intrested","Sligtly Intrested"),("Call Back","Call Back"))
    follow_up_status = models.CharField(max_length=20,default="Not Called",choices=options)
    follow_up_comments = models.TextField(max_length=1055)
    next_follow_up = models.DateField(auto_now_add=False)
    follow_up_by = models.ForeignKey(User,on_delete=models.DO_NOTHING)

    def __str__(self):

        return str(self.contact) + " contacted on " + str(self.date_of_follow_up)





