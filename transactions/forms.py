from django import forms
from .models import Invoice, InvoiceItem, Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'address']

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['customer', 'date_due', 'notes', 'status']
        widgets = {
            'date_due': forms.DateInput(attrs={'type': 'date'}),
        }

class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['product', 'unit_price']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate unit_price with product price as default
        

InvoiceItemFormSet = forms.inlineformset_factory(
    Invoice, InvoiceItem, form=InvoiceItemForm,
    extra=1, can_delete=True
)