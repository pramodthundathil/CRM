from django.urls import path 
from .import views  


urlpatterns = [
    path("AddContact",views.AddContact,name="AddContact"),
    path("import_data_from_excel",views.import_data_from_excel,name="import_data_from_excel"),
    path("PendingContacts",views.PendingContacts,name="PendingContacts"),
    path("ViewContactData/<int:pk>",views.ViewContactData,name="ViewContactData"),
    path("UpdateBasicData/<int:pk>",views.UpdateBasicData,name="UpdateBasicData"),
    path("FollowUpDateUpdate/<int:pk>",views.FollowUpDateUpdate,name="FollowUpDateUpdate"),
    path("lead_statusUpdate/<int:pk>/<str:strval>",views.lead_statusUpdate,name="lead_statusUpdate"),
    path("FollowUpUpadte/<int:pk>",views.FollowUpUpadte,name="FollowUpUpadte"),
    path("AssignContacts",views.AssignContacts,name="AssignContacts"),
    path("MyAssignments",views.MyAssignments,name="MyAssignments"),
    path("PendingTocall",views.PendingTocall,name="PendingTocall"),
    path("TodaysFollowUp",views.TodaysFollowUp,name="TodaysFollowUp"),
    path("UpcommingFollowUp",views.UpcommingFollowUp,name="UpcommingFollowUp"),
    path("WarmLeadsUser",views.WarmLeadsUser,name="WarmLeadsUser"),
    path("HotLeadsUser",views.HotLeadsUser,name="HotLeadsUser"),
    path("ConvertedLeads",views.ConvertedLeads,name="ConvertedLeads"),
    path("TodaysNewCalls",views.TodaysNewCalls,name="TodaysNewCalls"),
    path("UserWiseData",views.UserWiseData,name="UserWiseData"),
    path("CompletedToday",views.CompletedToday,name="CompletedToday"),
    path("Search",views.Search,name="Search"),
    path("UpdatesOfstaff/<int:pk>",views.UpdatesOfstaff,name="UpdatesOfstaff"),
    path("TodaysNewCallsAdmin/<int:pk>",views.TodaysNewCallsAdmin,name="TodaysNewCallsAdmin"),
    path("PendingTocallAdmin/<int:pk>",views.PendingTocallAdmin,name="PendingTocallAdmin"),
    path("TodaysFollowUpAdmin/<int:pk>",views.TodaysFollowUpAdmin,name="TodaysFollowUpAdmin"),
    path("MyAssignmentsAdmin/<int:pk>",views.MyAssignmentsAdmin,name="MyAssignmentsAdmin"),
    path("UpcommingFollowUpAdmin/<int:pk>",views.UpcommingFollowUpAdmin,name="UpcommingFollowUpAdmin"),
    path("CompletedTodayAdmin/<int:pk>",views.CompletedTodayAdmin,name="CompletedTodayAdmin"),
    path("AssignContactsSingle/<int:pk>",views.AssignContactsSingle,name="AssignContactsSingle"),
    path("FullDataReport",views.FullDataReport,name="FullDataReport"),
    path("MyReportTodaysFollowUp",views.MyReportTodaysFollowUp,name="MyReportTodaysFollowUp"),
    path("UpdatedDataAll",views.UpdatedDataAll,name="UpdatedDataAll"),
    path("DeleteContacts",views.DeleteContacts,name="DeleteContacts"),

    
  
]  