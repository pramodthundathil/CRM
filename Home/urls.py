from django.urls import path 
from .import views  
from .views import CustomLoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [

    # path("",views.SignIn,name="SignIn"),
    path("SignUp",views.SignUp,name="SignUp"),
    path("Index",views.Index,name="Index"),
    path("CompanyProfile",views.CompanyProfiles,name="CompanyProfile"),
    path('', CustomLoginView.as_view(), name='login'),
    path('logout', views.SignOut, name='logout'),
    path("SataffUserCreations",views.SataffUserCreations,name="SataffUserCreations"),
    path("Mytasks",views.Mytasks,name="Mytasks"),
    path("Settings",views.Settings,name="Settings"),
    path("ChangePassword",views.ChangePassword,name="ChangePassword")
    
]  