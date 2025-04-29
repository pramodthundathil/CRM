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