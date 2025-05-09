from django.urls import path
from . import views

# Use appropriate app name as per your project

# URLs for the reporting system
urlpatterns = [
    # Main reports page
    path('reports_page/', views.reports_page, name='reports_page'),
    
    # Export endpoints
    path('reports/export/all/', views.export_all_contacts, name='export_all_contacts'),
    path('reports/export/by-status/', views.export_by_status, name='export_by_status'),
    path('reports/export/by-lead-status/', views.export_by_lead_status, name='export_by_lead_status'),
    path('reports/export/follow-up-due/', views.export_follow_up_due, name='export_follow_up_due'),
    path('reports/export/by-staff/', views.export_by_staff, name='export_by_staff'),
    path('reports/export/conversions/', views.export_conversion_report, name='export_conversion_report'),
    path('reports/export/call-history/', views.export_call_history, name='export_call_history'),
    path('reports/export/activity/', views.export_activity_report, name='export_activity_report'),



    path('dashboard', views.dashboard, name='dashboard'),
    path('invoices/', views.invoice_list, name='invoice_list'),
    path('invoices/create/', views.create_invoice, name='create_invoice'),
    path('invoices/<int:pk>/', views.invoice_detail, name='invoice_detail'),
    path('invoices/<int:pk>/edit/', views.edit_invoice, name='edit_invoice'),
    path('invoices/<int:pk>/pdf/', views.GenerateInvoicePDF.as_view(), name='generate_invoice_pdf'),
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/create/', views.create_customer, name='create_customer'),
    path('customers/<int:pk>/edit/', views.edit_customer, name='edit_customer'),

]