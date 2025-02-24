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

from datetime import date, timedelta

def get_current_month_and_year():
    current_date = date.today()
    current_month = current_date.strftime("%B")
    current_year = current_date.year

    return current_month, current_year

# Usage
month, year = get_current_month_and_year()




# class CustomLoginView(LoginView):
#     template_name = 'login.html'  # specify your login template

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
        warm_contacts = StudentContact.objects.filter(lead_status = "Warm Lead",active = True).count()
        hot_contacts = StudentContact.objects.filter(lead_status = "Hot Lead",active = True).count()
        converted_contacts = StudentContact.objects.filter(lead_status = "Converted",active = True).count()
        rejected_contacts = StudentContact.objects.filter(active = False).count()
        pending = StudentContact.objects.filter(next_follow_up = date.today(),active = True).count()

        # lead status summery 
        notattended = StudentContact.objects.filter(follow_up_status = "Not Called",active = True).count()
        Intrested = StudentContact.objects.filter(follow_up_status = "Intrested",active = True).count()
        contacts = StudentContact.objects.filter(follow_up_status = "Intrested",active = True)
    else:
        contacts_count = StudentContact.objects.filter(lead_follow_up = request.user,active = True).count()
        warm_contacts = StudentContact.objects.filter(lead_follow_up = request.user,last_status = "Warm Lead",active = True).count()
        hot_contacts = StudentContact.objects.filter(lead_follow_up = request.user,last_status = "Hot Lead",active = True).count()
        converted_contacts = StudentContact.objects.filter(lead_status ='Converted').count()
        
        rejected_contacts = StudentContact.objects.filter(lead_follow_up = request.user,active = False).count()
        pending = StudentContact.objects.filter(lead_follow_up = request.user,next_follow_up__lt = date.today(),active = True).count()

        # lead status summery 
        notattended = StudentContact.objects.filter(lead_follow_up = request.user,follow_up_status = "Not Called",active = True).count()
        Intrested = StudentContact.objects.filter(lead_follow_up = request.user,follow_up_status = "Intrested",active = True).count()
        contacts = StudentContact.objects.filter(lead_follow_up = request.user,follow_up_status = "Intrested",active = True)





    # ++++++++++++++++++++++++++ Dash Board Chat components data start +++++++++++++++++++++++++++++++++++++
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    from django.db.models import Count
    from django.utils import timezone
    from django.db.models.functions import ExtractWeekDay, TruncMonth
    from datetime import timedelta 
    from django.db.models import Q, Count


    ############################ Calculations of Performace chart weekly wise start#############################
    # Get today's date
    today = timezone.now().date()
    # Calculate the start and end of the current week
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6)  # Sunday

    # Calculate the start and end of the previous week
    start_of_previous_week = start_of_week - timedelta(days=7)
    end_of_previous_week = end_of_week - timedelta(days=7)
     
    contacts_this_week = StudentContact.objects.filter(last_follow_up__range=[start_of_week, end_of_week]).exclude(follow_up_status = "Not Called")

    # Filter StudentContact objects for the previous week, excluding "Not Called"
    contacts_previous_week = StudentContact.objects.filter(last_follow_up__range=[start_of_previous_week, end_of_previous_week]).exclude(follow_up_status="Not Called")

    # Annotate and count the contacts day-wise
    day_wise_counts = contacts_this_week.annotate(day_of_week=ExtractWeekDay('last_follow_up')).values('day_of_week').annotate(count=Count('id')).order_by('day_of_week')

    # Annotate and count the contacts day-wise for the previous week
    day_wise_counts_previous_week = contacts_previous_week.annotate(day_of_week=ExtractWeekDay('last_follow_up')).values('day_of_week').annotate(count=Count('id')).order_by('day_of_week')



    # Create a dictionary to map day numbers to day names
    days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    day_wise_counts_dict_previous_week = {day: 0 for day in days}

    day_wise_counts_dict_this_week = {'Sunday':0,'Monday':0,'Tuesday':0,'Wednesday':0,'Thursday':0,'Friday':0,'Saturday':0}
    # day_wise_counts_dict = {days[entry['day_of_week'] - 1]: entry['count'] for entry in day_wise_counts}
    for entry in day_wise_counts:
        day_wise_counts_dict_this_week[days[entry['day_of_week'] - 1]] = entry['count']

    for entry in day_wise_counts_previous_week:
        day_wise_counts_dict_previous_week[days[entry['day_of_week'] - 1]] = entry['count']

    print(day_wise_counts_dict_this_week,",|--------------------------------------)")
    day_wise_counts_list_this_week = list(day_wise_counts_dict_this_week.values())
    print(day_wise_counts_list_this_week)
    day_wise_counts_list_previous_week = list(day_wise_counts_dict_previous_week.values())
    print(day_wise_counts_list_previous_week)
    ############################ Calculations of Performace chart weekly wise end #############################

    ############################ Calculation of donetchart monthly wise start this month #####################################
    sligtly_interested = StudentContact.objects.filter(follow_up_status = "Sligtly Intrested").count()
    interested = StudentContact.objects.filter(follow_up_status = "Intrested").count()
    not_called = StudentContact.objects.filter(follow_up_status = "Not Called").count()
    rejected = StudentContact.objects.filter(active = False).count()

    donut_list = [sligtly_interested,interested,not_called,rejected]
    print(donut_list,"-------------------------------")
    total_sum = sum(donut_list)

    # Calculate the percentage of each value in donut_list
    try:
        donut_list_percentages = [int((value / total_sum) * 100) for value in donut_list]
    except:
        donut_list_percentages = 0
    print(donut_list_percentages,"--------'''''''''''''''''''''''''''''''''''''''''''''''''''---------")


    ############################ Calculation of donetchart monthly wise end this month #####################################
    ############################ Calculation of Barchat month calling status start #####################################

    current_date = datetime.now()
    # Query to get the count of student contacts for each month and year
    monthly_counts = (
    StudentContact.objects
    .exclude(Q(follow_up_status='Intrested') | Q(follow_up_status='Sligtly Intrested') | Q(follow_up_status='Not Called'))
    .annotate(month=TruncMonth('last_follow_up'))
    .values('month')
    .annotate(count=Count('id'))
    .order_by('month')
)

    monthly_counts_interested = (
    StudentContact.objects
    .filter(Q(follow_up_status='Intrested') | Q(follow_up_status='Sligtly Intrested'))
    .annotate(month=TruncMonth('last_follow_up'))
    .values('month')
    .annotate(count=Count('id'))
    .order_by('month')
)
    # monthly_counts = (
    # StudentContact.objects
    # .all()
    # .annotate(month=TruncMonth('last_follow_up'))
    # .values('month')
    # .annotate(count=Count('id'))
    # .order_by('month')
    # )
    # print(monthly_counts,"44444444444444444444444444444444444444")
    # Extract the results into a list
    monthly_contact_counts = {"JAN":0,"FEB":0, "MAR":0, "APR":0, "MAY":0, "JUNE":0, "JUL":0, "AUG":0, "SEP":0, "OCT":0, "NOV":0, "DEC":0}
    monthly_contact_counts_interested = {"JAN":0,"FEB":0, "MAR":0, "APR":0, "MAY":0, "JUNE":0, "JUL":0, "AUG":0, "SEP":0, "OCT":0, "NOV":0, "DEC":0}
    for entry in monthly_counts:
        if entry['month'] == None:
            continue
        else:
            monthly_contact_counts[str((entry['month']).strftime("%B")).upper()] = entry["count"]


    for entry in monthly_counts_interested:
        if entry['month'] == None:
            continue
        else:
            monthly_contact_counts_interested[str((entry['month']).strftime("%B")).upper()] = entry["count"]

        # print(str((entry['month']).strftime("%B")).upper(),"00000000000000000000000000000000000000000")

    # print(monthly_contact_counts,"88888888888888888888888888888888888888888888888888888888888888888")
    ongoing = list(monthly_contact_counts.values())
    interested_contact_count = list(monthly_contact_counts_interested.values())
    # print(interested_contact_count,"oioisadah777777777777777777777777777777777777777777777777777777")


    ############################ Calculation of Barchat month calling status end #####################################
    ############################ Calculation of Performence status Start #####################################
    """
    Performence Analyser Createria:
    Calculate the the total calls of a day (Includes all call data ).
    also monthly interested and slightly interested data and covertions of leads will be 30% of contribution in the calculation
    70% point will be from total called data.

    """

    users = User.objects.get(id = 3)
    # Get the first and last days of the current month
    current_date = date.today()
    first_day_of_month = current_date.replace(day=1)
    last_day_of_month = current_date.replace(day=1, month=current_date.month % 12 + 1) - timedelta(days=1)
    
    
    users_count = (
    StudentContact.objects
    .exclude(last_follow_up=None)  # Exclude objects where last_follow_up is None
    .exclude(follow_up_status='Not Called')
    .filter(last_follow_up__range=[first_day_of_month, last_day_of_month])  # Filter by last_follow_up within current month
    .values('lead_follow_up')  # Group by lead_follow_up foreign key
    .annotate(count=Count('lead_follow_up'))  # Count occurrences of each lead_follow_up
    )
    # print(User.objects.get(id = users_count[1]["lead_follow_up"]),",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,")
    # Create a dictionary with foreign key objects as keys and their counts as values
    foreign_key_count_dict = {}
    for item in users_count:
        foreign_key = item['lead_follow_up']
        count = item['count']
        foreign_key_object = User.objects.get(id=foreign_key)
        foreign_key_count_dict[foreign_key_object] = count
        sorted_foreign_key_count_dict = dict(sorted(foreign_key_count_dict.items(), key=lambda item: item[1], reverse=True))

    # print(list(foreign_key_count_dict.keys())[0].first_name)
    # print(sorted_foreign_key_count_dict)

    # rankwisedict = sorted_foreign_key_count_dict

    # print((sorted_foreign_key_count_dict.keys()))
    
    


    ############################ Calculation of Performence status End #######################################

    

    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # ++++++++++++++++++++++++++ Dash Board Chat components data end +++++++++++++++++++++++++++++++++++++
    # 
    # 
    # "performence_data":rankwisedict,
    
    
    context = {
        "month":month,
        "year":year,
        "contacts":contacts[:10],
        "contacts_count":contacts_count,
        "warm_contacts":warm_contacts,
        "hot_contacts":hot_contacts,
        "converted_contacts":converted_contacts,
        "rejected_contacts":rejected_contacts,
        "pending":pending,
        "notattended":notattended,
        "Intrested":Intrested,

        # Chart Values To the templates
        #$$ for line chart  .....
        "day_wise_counts_list_this_week":day_wise_counts_list_this_week,
        "day_wise_counts_list_previous_week":day_wise_counts_list_previous_week,
        #$$ for donut chat ......
        "donut_list_percentages":donut_list_percentages,
        "ongoing":ongoing,
        "interested_contact_count":interested_contact_count,
        



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





