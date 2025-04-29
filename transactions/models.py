from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime

class Customer(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name



class Invoice(models.Model):
    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('SENT', 'Sent'),
        ('PAID', 'Paid'),
        ('CANCELLED', 'Cancelled'),
    )
    
    invoice_number = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_due = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.invoice_number
    
    def get_total(self):
        return sum(item.get_total() for item in self.invoiceitem_set.all())
    
    def save(self, *args, **kwargs):
        if not self.invoice_number:
            # Generate invoice number format: INV-YEAR-MONTH-XXXX
            year_month = datetime.now().strftime("%Y%m")
            last_invoice = Invoice.objects.filter(invoice_number__startswith=f"INV-{year_month}").order_by('invoice_number').last()
            if last_invoice:
                last_number = int(last_invoice.invoice_number.split('-')[-1])
                self.invoice_number = f"INV-{year_month}-{last_number + 1:04d}"
            else:
                self.invoice_number = f"INV-{year_month}-0001"
        super().save(*args, **kwargs)

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    product = models.CharField(max_length=1000)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def get_total(self):
        return  self.unit_price
    
    def __str__(self):
        return f"{self.product} - {self.invoice.invoice_number}"