from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from Contacts.models import StudentContact, LeadCallStatus
from datetime import datetime, timedelta
import pandas as pd
from django.db.models import Count, Q
from django.utils import timezone
from django.contrib.auth.models import User

# Update the reports_page view to include users for the staff selection dropdown
def reports_page(request):
    """Render the reports page with necessary context"""
    # Get all users for staff reports dropdown
    users = User.objects.filter(is_active=True)
    
    context = {
        'users': users
    }
    
    return render(request, 'reports.html', context)

@login_required
def export_all_contacts(request):
    """Export all contacts to Excel"""
    # Get all active contacts
    contacts = StudentContact.objects.filter(active=True)
    
    # Create DataFrame
    data = []
    for contact in contacts:
        data.append({
            'Name': contact.name,
            'Contact Number': contact.contact_number,
            'Email': contact.email,
            'Study Stream': contact.study_streem,
            'College': contact.collage,
            'DOB': contact.DOB,
            'Date Added': contact.added_date,
            'Last Follow Up': contact.last_follow_up,
            'Number of Follow Ups': contact.number_follow_up,
            'Follow Up Status': contact.follow_up_status,
            'Last Status': contact.last_status,
            'Next Follow Up': contact.next_follow_up,
            'Lead Status': contact.lead_status,
            'Assigned To': contact.lead_follow_up.username if contact.lead_follow_up else 'Not Assigned'
        })
    
    df = pd.DataFrame(data)
    
    # Create Excel response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=all_contacts.xlsx'
    
    # Convert DataFrame to Excel
    df.to_excel(response, index=False)
    
    return response

@login_required
def export_by_status(request):
    """Export contacts by follow-up status"""
    status = request.GET.get('status', 'Not Called')
    
    # Get contacts by status
    contacts = StudentContact.objects.filter(follow_up_status=status, active=True)
    
    # Create DataFrame
    data = []
    for contact in contacts:
        data.append({
            'Name': contact.name,
            'Contact Number': contact.contact_number,
            'Email': contact.email,
            'Study Stream': contact.study_streem,
            'College': contact.collage,
            'Last Follow Up': contact.last_follow_up,
            'Next Follow Up': contact.next_follow_up,
            'Lead Status': contact.lead_status,
            'Assigned To': contact.lead_follow_up.username if contact.lead_follow_up else 'Not Assigned'
        })
    
    df = pd.DataFrame(data)
    
    # Create Excel response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=contacts_by_status_{status}.xlsx'
    
    # Convert DataFrame to Excel
    df.to_excel(response, index=False)
    
    return response

@login_required
def export_by_lead_status(request):
    """Export contacts by lead status"""
    lead_status = request.GET.get('lead_status', 'Warm Lead')
    
    # Get contacts by lead status
    contacts = StudentContact.objects.filter(lead_status=lead_status, active=True)
    
    # Create DataFrame
    data = []
    for contact in contacts:
        data.append({
            'Name': contact.name,
            'Contact Number': contact.contact_number,
            'Email': contact.email,
            'Study Stream': contact.study_streem,
            'College': contact.collage,
            'Follow Up Status': contact.follow_up_status,
            'Last Status': contact.last_status,
            'Next Follow Up': contact.next_follow_up,
            'Assigned To': contact.lead_follow_up.username if contact.lead_follow_up else 'Not Assigned'
        })
    
    df = pd.DataFrame(data)
    
    # Create Excel response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=contacts_by_lead_status_{lead_status}.xlsx'
    
    # Convert DataFrame to Excel
    df.to_excel(response, index=False)
    
    return response

@login_required
def export_follow_up_due(request):
    """Export contacts with follow-up due today or overdue"""
    today = timezone.now().date()
    
    # Get contacts with follow-up due today or overdue
    contacts = StudentContact.objects.filter(
        Q(next_follow_up__lte=today) & 
        ~Q(follow_up_status__in=['Not intrested', 'Converted']) & 
        Q(active=True)
    )
    
    # Create DataFrame
    data = []
    for contact in contacts:
        data.append({
            'Name': contact.name,
            'Contact Number': contact.contact_number,
            'Email': contact.email,
            'Follow Up Status': contact.follow_up_status,
            'Next Follow Up': contact.next_follow_up,
            'Days Overdue': (today - contact.next_follow_up).days if contact.next_follow_up else 'N/A',
            'Lead Status': contact.lead_status,
            'Assigned To': contact.lead_follow_up.username if contact.lead_follow_up else 'Not Assigned'
        })
    
    df = pd.DataFrame(data)
    
    # Create Excel response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=follow_up_due.xlsx'
    
    # Convert DataFrame to Excel
    df.to_excel(response, index=False)
    
    return response

@login_required
def export_by_staff(request):
    """Export contacts assigned to a specific staff member"""
    staff_id = request.GET.get('staff_id')
    
    if not staff_id:
        # Return all contacts grouped by staff
        contacts = StudentContact.objects.filter(active=True)
        
        # Create DataFrame
        data = []
        for contact in contacts:
            data.append({
                'Name': contact.name,
                'Contact Number': contact.contact_number,
                'Email': contact.email,
                'Follow Up Status': contact.follow_up_status,
                'Lead Status': contact.lead_status,
                'Next Follow Up': contact.next_follow_up,
                'Assigned To': contact.lead_follow_up.username if contact.lead_follow_up else 'Not Assigned'
            })
        
        df = pd.DataFrame(data)
        
        # Create Excel response
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=contacts_by_staff.xlsx'
        
        # Convert DataFrame to Excel with staff as sheet name
        with pd.ExcelWriter(path=response, engine='openpyxl') as writer:
            # Group by assigned staff and create a sheet for each
            if not df.empty:
                for staff, group in df.groupby('Assigned To'):
                    sheet_name = staff[:31] if staff else 'Unassigned'  # Excel has a 31 character limit for sheet names
                    group.to_excel(writer, sheet_name=sheet_name, index=False)
            else:
                df.to_excel(writer, sheet_name='No Data', index=False)
        
        return response
    else:
        # Get contacts assigned to specific staff
        contacts = StudentContact.objects.filter(lead_follow_up_id=staff_id, active=True)
        
        # Create DataFrame
        data = []
        for contact in contacts:
            data.append({
                'Name': contact.name,
                'Contact Number': contact.contact_number,
                'Email': contact.email,
                'Study Stream': contact.study_streem,
                'College': contact.collage,
                'Follow Up Status': contact.follow_up_status,
                'Lead Status': contact.lead_status,
                'Last Follow Up': contact.last_follow_up,
                'Next Follow Up': contact.next_follow_up
            })
        
        df = pd.DataFrame(data)
        
        # Create Excel response
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=contacts_by_staff_{staff_id}.xlsx'
        
        # Convert DataFrame to Excel
        df.to_excel(response, index=False)
        
        return response

@login_required
def export_conversion_report(request):
    """Export conversion report showing leads converted over time"""
    # Get date range from request or default to last 30 days
    days = int(request.GET.get('days', 30))
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=days)
    
    # Get all conversion activities
    converted_leads = LeadCallStatus.objects.filter(
        contact__lead_status='Converted',
        date_of_follow_up__date__gte=start_date,
        date_of_follow_up__date__lte=end_date
    ).values('follow_up_by__username').annotate(count=Count('id'))
    
    # Create DataFrame for conversion by staff
    conversion_by_staff = []
    for lead in converted_leads:
        conversion_by_staff.append({
            'Staff': lead['follow_up_by__username'],
            'Conversions': lead['count']
        })
    
    # Create DataFrame for daily conversions
    daily_data = []
    current_date = start_date
    while current_date <= end_date:
        count = LeadCallStatus.objects.filter(
            contact__lead_status='Converted',
            date_of_follow_up__date=current_date
        ).count()
        
        daily_data.append({
            'Date': current_date,
            'Conversions': count
        })
        current_date += timedelta(days=1)
    
    df_by_staff = pd.DataFrame(conversion_by_staff)
    df_daily = pd.DataFrame(daily_data)
    
    # Create Excel response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=conversion_report_{start_date}_to_{end_date}.xlsx'
    
    # Write both DataFrames to different sheets
    with pd.ExcelWriter(path=response, engine='openpyxl') as writer:
        df_by_staff.to_excel(writer, sheet_name='By Staff', index=False)
        df_daily.to_excel(writer, sheet_name='Daily Conversions', index=False)
    
    return response

@login_required
def export_call_history(request):
    """Export detailed call history for a specific contact"""
    contact_id = request.GET.get('contact_id')
    
    if not contact_id:
        return HttpResponse("Contact ID is required", status=400)
    
    # Get contact
    try:
        contact = StudentContact.objects.get(id=contact_id)
    except StudentContact.DoesNotExist:
        return HttpResponse("Contact not found", status=404)
    
    # Get call history
    call_history = LeadCallStatus.objects.filter(contact=contact).order_by('-date_of_follow_up')
    
    # Create DataFrame
    data = []
    for call in call_history:
        data.append({
            'Date': call.date_of_follow_up,
            'Status': call.follow_up_status,
            'Comments': call.follow_up_comments,
            'Next Follow Up': call.next_follow_up,
            'Called By': call.follow_up_by.username
        })
    
    df = pd.DataFrame(data)
    
    # Add contact info to a separate sheet
    contact_info = [{
        'Name': contact.name,
        'Contact Number': contact.contact_number,
        'Email': contact.email,
        'Study Stream': contact.study_streem,
        'College': contact.collage,
        'DOB': contact.DOB,
        'Date Added': contact.added_date,
        'Current Status': contact.follow_up_status,
        'Lead Status': contact.lead_status,
        'Number of Follow Ups': contact.number_follow_up,
        'Assigned To': contact.lead_follow_up.username if contact.lead_follow_up else 'Not Assigned'
    }]
    
    df_info = pd.DataFrame(contact_info)
    
    # Create Excel response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=call_history_{contact.name}.xlsx'
    
    # Write both DataFrames to different sheets
    with pd.ExcelWriter(path=response, engine='openpyxl') as writer:
        df_info.to_excel(writer, sheet_name='Contact Info', index=False)
        df.to_excel(writer, sheet_name='Call History', index=False)
    
    return response

@login_required
def export_activity_report(request):
    """Export activity report showing calls made by staff members"""
    # Get date range from request or default to last 7 days
    days = int(request.GET.get('days', 7))
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=days)
    
    # Get all call activities
    calls = LeadCallStatus.objects.filter(
        date_of_follow_up__date__gte=start_date,
        date_of_follow_up__date__lte=end_date
    )
    
    # Create DataFrame for calls by staff
    data = []
    for call in calls:
        data.append({
            'Date': call.date_of_follow_up.date(),
            'Staff': call.follow_up_by.username,
            'Contact': call.contact.name,
            'Status': call.follow_up_status,
            'Comments': call.follow_up_comments
        })
    
    df = pd.DataFrame(data)
    
    # Create a summary DataFrame
    if not df.empty:
        summary = df.groupby(['Staff', 'Status']).size().unstack(fill_value=0)
        summary['Total Calls'] = summary.sum(axis=1)
        
        # Add daily summary by staff
        daily_summary = df.groupby(['Date', 'Staff']).size().unstack(fill_value=0)
    else:
        summary = pd.DataFrame(columns=['Total Calls'])
        daily_summary = pd.DataFrame()
    
    # Create Excel response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=activity_report_{start_date}_to_{end_date}.xlsx'
    
    # Write DataFrames to different sheets
    with pd.ExcelWriter(path=response, engine='openpyxl') as writer:
        if not df.empty:
            summary.to_excel(writer, sheet_name='Summary')
            daily_summary.to_excel(writer, sheet_name='Daily Summary')
        df.to_excel(writer, sheet_name='All Calls', index=False)
    
    return response




# invoice generation 


from django.http import JsonResponse




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from django.views import View
from django.utils.decorators import method_decorator
from Home.models import CompanyProfile

from .models import Invoice, InvoiceItem, Customer
from .forms import InvoiceForm, InvoiceItemFormSet, CustomerForm

@login_required
def dashboard(request):
    invoices = Invoice.objects.all().order_by('-date_created')
    total_invoices = invoices.count()
    pending_invoices = invoices.filter(status='SENT').count()
    paid_invoices = invoices.filter(status='PAID').count()
    
    context = {
        'invoices': invoices[:10],  # Show only 10 latest invoices
        'total_invoices': total_invoices,
        'pending_invoices': pending_invoices,
        'paid_invoices': paid_invoices,
    }
    return render(request, 'invoices/dashboard.html', context)

@login_required
def invoice_list(request):
    invoices = Invoice.objects.all().order_by('-date_created')
    return render(request, 'invoices/invoice_list.html', {'invoices': invoices})

@login_required
def create_invoice(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.created_by = request.user
            invoice.save()
            
            formset = InvoiceItemFormSet(request.POST, instance=invoice)
            if formset.is_valid():
                formset.save()
                messages.success(request, 'Invoice created successfully.')
                return redirect('invoice_detail', pk=invoice.pk)
    else:
        form = InvoiceForm()
        formset = InvoiceItemFormSet()
    
    context = {
        'form': form,
        'formset': formset,
        'customers': Customer.objects.all(),
        
    }
    return render(request, 'invoices/invoice_form.html', context)

@login_required
def edit_invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    
    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            form.save()
            
            formset = InvoiceItemFormSet(request.POST, instance=invoice)
            if formset.is_valid():
                formset.save()
                messages.success(request, 'Invoice updated successfully.')
                return redirect('invoice_detail', pk=invoice.pk)
    else:
        form = InvoiceForm(instance=invoice)
        formset = InvoiceItemFormSet(instance=invoice)
    
    context = {
        'form': form,
        'formset': formset,
        'invoice': invoice,
        'customers': Customer.objects.all(),
        
    }
    return render(request, 'invoices/invoice_form.html', context)

@login_required
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    return render(request, 'invoices/invoice_detail.html', {'invoice': invoice})

@method_decorator(login_required, name='dispatch')
class GenerateInvoicePDF(View):
    def get(self, request, pk):
        invoice = get_object_or_404(Invoice, pk=pk)
        company_profile = CompanyProfile.objects.all().last()
        
        # Create a context dictionary with all necessary data
        template = get_template('invoices/invoice_pdf.html')
        context = {
            'invoice': invoice,
            'company': {
                'name': 'Byte Boot Techno Solutions Pvt Ltd',
                'address': 'Your Company Address',  # Add your address here
                'phone': 'Your Company Phone',      # Add your phone here
                'email': 'Your Company Email',
                'website': 'Your Company Website',
            },
            "company_profile": company_profile
        }
        
        # Convert relative image paths to absolute file system paths
        html = template.render(context)
        
        # Configure PDF options for better handling of images and CSS
        pdf_options = {
            "encoding": "UTF-8",
            "warn": True,  # Show warnings during PDF generation
            "link_callback": fetch_resources,  # Use a custom resource loader (defined below)
        }
        
        # Create PDF
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result, **pdf_options)
        
        if not pdf.err:
            response = HttpResponse(result.getvalue(), content_type='application/pdf')
            filename = f"Invoice_{invoice.invoice_number}.pdf"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
        
        # If there's an error, print it for debugging
        print(f"PDF Generation Error: {pdf.err}")
        return HttpResponse("Error generating PDF", status=400)

# Helper function to resolve resources (especially images)
def fetch_resources(uri, rel):
    """
    Convert HTML URIs to absolute system paths so pisa can access those resources
    """
    from django.conf import settings
    import os.path
    
    # Convert URIs starting with MEDIA_URL or STATIC_URL to absolute paths
    if uri.startswith(settings.MEDIA_URL):
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    elif uri.startswith(settings.STATIC_URL):
        path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ""))
    else:
        # Handle relative paths referenced in the HTML
        path = os.path.join(settings.BASE_DIR, uri)
    
    # Return the absolute path to the resource
    return path

@login_required
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'invoices/customer_list.html', {'customers': customers})

@login_required
def create_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer created successfully.')
            return redirect('customer_list')
    else:
        form = CustomerForm()
    
    return render(request, 'invoices/customer_form.html', {'form': form})

@login_required
def edit_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer updated successfully.')
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    
    return render(request, 'invoices/customer_form.html', {'form': form, 'customer': customer})

