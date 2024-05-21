from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserAddForm
from django.contrib.auth.models import User, Group
from .decorators import admin_only, unautenticated_user
from django.contrib.auth.views import LoginView

from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from datetime import date, datetime
from django.contrib.auth.decorators import login_required

# models import 

from .models import CompanyProfile
from Contacts.models import StudentContact, LeadCallStatus 

class CustomLoginView(LoginView):
    template_name = 'login.html'  # specify your login template

# # Create your views here.
# @unautenticated_user
# def SignIn(request):
#     if request.method == "POST":
#         username = request.POST['uname']
#         password = request.POST['pswd']
#         user1 = authenticate(request, username = username , password = password)
        
#         if user1 is not None:
            
#             request.session['username'] = username
#             request.session['password'] = password
#             login(request, user1)
#             return redirect('Index')
        
#         else:
#             messages.info(request,'Username or Password Incorrect')
#             return redirect('SignIn')
#     return render(request,"login.html")


# authetication an d log out functions starts................................
@unautenticated_user
def SignUp(request):
    form = UserAddForm()
    if request.method == "POST":
        # fname = request.POST["fname"]
        # email = request.POST["email"]
        # uname = request.POST["uname"]
        # pswd = request.POST["pswd"]
        # pswd1 = request.POST["pswd1"]

        # if pswd != pswd1:
        #     messages.info(request,"Password Do not Matches..")
        #     return redirect("SignUp")
        # if User.objects.filter(username = uname).exists():
        #     messages.info(request,"Username alredy exists user another username")
        #     return redirect("SignUp")
        # if User.objects.filter(email = email).exists():
        #     messages.info(request,"Email alredy exists user another email")
        #     return redirect("SignUp")

        form = UserAddForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.save()
            group = Group.objects.get(name='student')
            user.groups.add(group)
            messages.success(request,"User Created.. Please Login....")
            return redirect("SignIn")
        
    return render(request,"register.html",{"form":form})


def SignOut(request):
    logout(request)
    return redirect('login')


# index pages and utilities area 

class CustomLoginView(LoginView):
    template_name = 'login.html'  # specify your login template

    def get_success_url(self):
        # Customize the behavior after login here
        # For example, redirect to a specific URL
        return reverse_lazy('Index')  # 'profile' should be replaced with the name of your desired URL pattern


# authentication and log out end ....................................


@login_required(login_url="login")
def Index(request):
    if request.user.groups.all()[0].name == "admin":
        contacts_count = StudentContact.objects.filter(active = True).count()
        warm_contacts = StudentContact.objects.filter(last_status = "Warm Lead",active = True).count()
        hot_contacts = StudentContact.objects.filter(last_status = "Hot Lead",active = True).count()
        converted_contacts = StudentContact.objects.filter(last_status = "Converted",active = True).count()
        rejected_contacts = StudentContact.objects.filter(last_status = "Rejected",active = True).count()
        pending = StudentContact.objects.filter(next_follow_up = date.today(),active = True).count()
    else:
        contacts_count = StudentContact.objects.filter(lead_follow_up = request.user,active = True).count()
        warm_contacts = StudentContact.objects.filter(lead_follow_up = request.user,last_status = "Warm Lead",active = True).count()
        hot_contacts = StudentContact.objects.filter(lead_follow_up = request.user,last_status = "Hot Lead",active = True).count()
        converted_contacts = StudentContact.objects.filter(lead_follow_up = request.user,last_status = "Converted",active = True).count()
        rejected_contacts = StudentContact.objects.filter(lead_follow_up = request.user,last_status = "Rejected",active = True).count()
        pending = StudentContact.objects.filter(lead_follow_up = request.user,next_follow_up__lt = date.today(),active = True).count()

    
    context = {
        "contacts_count":contacts_count,
        "warm_contacts":warm_contacts,
        "hot_contacts":hot_contacts,
        "converted_contacts":converted_contacts,
        "rejected_contacts":rejected_contacts,
        "pending":pending

    }
    return render(request,"index.html",context)


# company profile creation 
@login_required(login_url="login")
def CompanyProfiles(request):
    # getting company profile data.....................
    profile = CompanyProfile.objects.filter(user = request.user).first()

    if request.method == "POST":
        name = request.POST.get("cname")
        email = request.POST.get("email")
        City = request.POST.get("city")
        dis = request.POST.get("dis")
        logo = request.FILES.get("logo")

        print(logo)
        if CompanyProfile.objects.filter(user = request.user).exists():
            profi = CompanyProfile.objects.get(user = request.user)
            profi.Company_Name = name
            profi.email = email
            profi.City = City
            profi.Company_Profile_Description = dis 
            if logo != None:
                profi.Company_Logo.delete()
                profi.Company_Logo = logo
            profi.save()
            messages.info(request,"Data Updated Successfully")
            return redirect("CompanyProfile")
        else:
            profi = CompanyProfile.objects.create(Company_Name = name, email = email, City = City,Company_Profile_Description = dis,Company_Logo = logo )
            profi.user.add(request.user)
            profi.save()
            messages.info(request,"Data Updated Successfully")
            return redirect("CompanyProfile")

    context = {
        "profile":profile
    }

    return render(request,"company_profile.html",context)


@login_required(login_url="login")
def SataffUserCreations(request):
    companyprofile = CompanyProfile.objects.get(user = request.user)
    staff =  companyprofile.user.all()
    if request.method == "POST":
        fname = request.POST["fname"]
        email = request.POST["email"]
        uname = request.POST["uname"]
        pswd = request.POST["pswd"]
        pswd1 = request.POST["pswd1"]
        mnum = request.POST['mnum']
        utype = request.POST['utype']

        if pswd != pswd1:
            messages.info(request,"Password Do not Matches..")
            return redirect("SataffUserCreations")
        if User.objects.filter(username = uname).exists():
            messages.info(request,"Username alredy exists user another username")
            return redirect("SataffUserCreations")
        if User.objects.filter(email = email).exists():
            messages.info(request,"Email alredy exists user another email")
            return redirect("SataffUserCreations")
        else:
            user = User.objects.create_user(first_name = fname,email = email, username = uname, password =pswd)
            user.save()
            companyprofile = CompanyProfile.objects.get(user = request.user)
            companyprofile.user.add(user)
            companyprofile.save()

            group = Group.objects.get(name=utype)
            user.groups.add(group)
            messages.info(request,"Staff added To Staff list....")
            return redirect("SataffUserCreations")

    context = {
        "staff":staff
    }
    return render(request,'Staff/addstaff.html',context)

@login_required(login_url="login")
def Mytasks(request):
    contact_count = StudentContact.objects.filter(lead_follow_up = request.user,follow_up_status = "Not Called",active = True ).count()
    new_contact_count = StudentContact.objects.filter(lead_follow_up = request.user,follow_up_status = "Not Called", next_follow_up = date.today(),active = True ).count()
    penidng_call_list = StudentContact.objects.filter(lead_follow_up = request.user,next_follow_up__lt = date.today(),active = True).count()
    today_follow_up = StudentContact.objects.filter(lead_follow_up = request.user,next_follow_up = date.today(),active = True).exclude(follow_up_status = "Not Called").count()
    upcomming_contacts_count = StudentContact.objects.filter(lead_follow_up = request.user,next_follow_up__gt = date.today(),active = True).count()
    today_contacts_completed = StudentContact.objects.filter(lead_follow_up = request.user,last_follow_up = date.today()).count()
    rejected_contacts = StudentContact.objects.filter(lead_follow_up = request.user,active = False).count()
    all_contacts = StudentContact.objects.filter(lead_follow_up = request.user,active = True).count()
    



    context = {
        "contact_count":contact_count,
        "penidng_call_list":penidng_call_list,
        "today_follow_up":today_follow_up,
        "new_contact_count":new_contact_count,
        "upcomming_contacts_count":upcomming_contacts_count,
        "today_contacts_completed":today_contacts_completed,
        "rejected_contacts":rejected_contacts,
        "all_contacts":all_contacts
    }
    return render(request,"todaystasks.html",context)


@login_required(login_url="login")
def Settings(request):
    return render(request,"settings.html")

@login_required(login_url='login')
def ChangePassword(request):
    if request.method == "POST":
        oldpass = request.POST["cpswd"]
        newpass1 = request.POST['npswd']
        newpass2 = request.POST['nconpswd']
        user1 = authenticate(request,username = request.user.username,password = oldpass)
        if user1 is not None:
            if newpass1 == newpass2:
                user  = request.user 
                user.set_password(newpass1)
                user.save()
                messages.success(request, "Password Change Success Please Login To Continue..")
                return redirect("Settings")
            else:
                messages.error(request, "Password not Matching..")
                return redirect("Settings")
        else:
            messages.error(request, "Password is incorrect")
            return redirect("Settings")

    return redirect("Settings")





