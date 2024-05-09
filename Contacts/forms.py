from django import forms
from .models import StudentContact
from datetime import date

today = date.today()

class StudentContactForm(forms.ModelForm):
    class Meta:
        model = StudentContact
        exclude = ['added_date', 'follow_up_started_date', 'last_follow_up', 'number_follow_up', 'active', 'lead_follow_up']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={"type":"number", 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'study_streem': forms.TextInput(attrs={'class': 'form-control'}),
            'collage': forms.TextInput(attrs={'class': 'form-control'}),
            'DOB': forms.DateInput(attrs={'class': 'form-control', "type":"date","max":today }),
            'follow_up_status': forms.Select(attrs={'class': 'form-control'}),
            'last_status': forms.Textarea(attrs={ 'rows': 4,"col":10}),
            'next_follow_up': forms.DateInput(attrs={'class': 'form-control',"type":"date","min":today}),
            'lead_status': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_contact_number(self):
        contact_number = self.cleaned_data.get('contact_number')
        if contact_number and len(str(contact_number)) != 10:
            raise forms.ValidationError("Contact number must be 10 digits.")
        return contact_number
