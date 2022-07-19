from management.models import Student
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# FOR WEASY PRINT pdf zote
from django.template.loader import render_to_string
from weasyprint import HTML
from datetime import datetime
import tempfile
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
import requests

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from . forms import UserRegistrationForm,ProfileForm
from .models import Profile ,TermsAndConditions,User
from management.models import *
from fee.models import *
from expenses.models import *


def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request,'accounts/index.html')

def registeruser(request):
    if request.user.is_authenticated:
        return redirect("dashboard") 
    form=UserRegistrationForm()
    if request.method=="POST":
      form=UserRegistrationForm(request.POST)
      if form.is_valid():
            form.save()
            user=str(form.cleaned_data.get('email'))
            messages.success(request,'Dear '+ user + ' Registration Is Successful !')
            msg='Dear ' + user + 'Registration Completed Successfully welcome to Mayfair Academy Web Admin'
            send_mail(
            'Mayfair Academy Web Admin',
            msg,
            settings.EMAIL_HOST_USER,
            [user],
            fail_silently=False,
            )
            inf='Another User with Email Address : ' + user + ' Has Registerd  ' 
            send_mail(
            ' Mayfair Academy Web Admin ',
            inf,
            settings.EMAIL_HOST_USER,
            ['applymayfair@gmail.com'],
            fail_silently=False,
            )
            return redirect('loginuser')
    return render (request,'accounts/register.html',{'form':form})

def loginuser(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method=="POST":
        registration_number = request.POST.get('registration_number')
        password = request.POST.get('password')
        userlogin = authenticate(request, registration_number=registration_number, password=password)
        if userlogin is not None:
            login(request, userlogin)
            return redirect('dashboard')
        else:
            messages.info( request, 'Registration number or password incorrect')
            return redirect('loginuser')
    return render (request,'accounts/login.html')


# here you were haaving two dashboard view , this mine , yours is down there 
# @login_required(login_url='loginuser')
# def dashboard(request):
#     settings=Setting.objects.all().count()

#     print(settings,'seeeeeeeeeeeeeeeeeeeeeeeeeee')
#     if settings == 0 : 
#         return redirect('configuration_one')
#     if request.user.is_superuser:
#         student_count=Student.objects.all().count()
#         teachers_count=Staff.objects.filter(role="teacher").count()
#         superuser_count=Staff.objects.filter(role="superuser").count()
#         accountant_count=Staff.objects.filter(role="acountant").count()
#     else:
#         student_count=0
#         teachers_count=0
#         superuser_count=0
#         accountant_count=0
#     print(student_count,teachers_count,superuser_count,accountant_count,'dddddddddddddddddddddddddddd')

   
    # return render (request,'accounts/dashboard.html', {'student_count':student_count,'teachers_count':teachers_count,'superuser_count':superuser_count,'accountant_count':accountant_count})


@login_required(login_url='loginuser')
def profile(request):
    form=ProfileForm()
    return render(request,'accounts/profile.html',{'form':form})

@login_required(login_url='loginuser')
def updateprofile(request,pk):
    form=ProfileForm(instance=request.user.profile)
    if request.method=="POST":
        form=ProfileForm(request.POST,request.FILES,instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.info(request,'Your Profile Information Has Been Successfully Updated ')
            return redirect('viewprofile')   
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request,'accounts/profile.html',{'form':form})

@login_required(login_url='loginuser')
def viewprofile(request):
    profile_objects=Profile.objects.filter(user=request.user)
    return render(request,'accounts/viewprofile.html',{'profile_objects':profile_objects})

def logoutuser(request):
    logout(request)
    messages.info( request, 'Bye Successfully Logged out !!')
    return redirect('loginuser') 

@login_required(login_url='loginuser')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # update pass yenye ilikuwa james 
            messages.success(request, 'Your password was successfully updated!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })

def term_and_condations_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    terms=TermsAndConditions.objects.all()
    terms_count=terms.count()
    return render(request,'accounts/term_and_condations.html',{'terms':terms,'terms_count':terms_count})



@login_required(login_url='loginuser')
def dashboard(request):
    # be protecting functions by checking who is logged in
    if request.user.is_superuser:
        student_count=Student.objects.all().count()
        teachers_count=Staff.objects.filter(role="teacher").count()
        superuser_count=Staff.objects.filter(role="superuser").count()
        accountant_count=Staff.objects.filter(role="acountant").count()
    else:
        student_count=0
        teachers_count=0
        superuser_count=0
        accountant_count=0

    school_expenses=SchoolExpenses.objects.all().order_by('-date_requested')
    school_assets=SchoolAssets.objects.all().order_by('-date_added')
    school_fees=Payment.objects.all().order_by('-date_added')

# expenses
    total_expe=0
    for x in school_expenses:
        total_expe= total_expe + x.item_cost

    #dont use + 100 on this  
    #Total fees
    total_fee=0
    for x in school_fees:
        total_fee = total_fee + x.amount_paid

    #Toatal Asserts
    total_asset=0
    for x in school_assets:
        total_asset= total_asset + x.asset_value


    # dealing with dates 
    current_day = datetime.now().day
    current_month = datetime.now().month
    current_year = datetime.now().year 

    #Daily Fees Collection
    fee_this_day = Payment.objects.filter(date_added__day=current_day)
    this_day_total=0

    for x in fee_this_day:
        this_day_total = this_day_total + x.amount_paid

    #Monthly Fees Collection
    fee_this_month=Payment.objects.filter(date_added__month=current_month)
    this_month_total=0

    for x in fee_this_month:
        this_month_total = this_month_total + x.amount_paid

    #Annual Fees Collection
    fee_this_year=Payment.objects.filter(date_added__year=current_year)
    this_year_total=0

    for x in fee_this_year:
        this_year_total = this_year_total + x.amount_paid

    #Daily Expenses Records
    exp_this_day = SchoolExpenses.objects.filter(date_requested__day=current_day)
    this_day_exp_total = 0

    for x in exp_this_day:
        this_day_exp_total = this_day_exp_total + x.item_cost


    #Monthly Expenses Records
    exp_this_month = SchoolExpenses.objects.filter(date_requested__month=current_month)
    this_month_exp_total = 0

    for x in exp_this_month:
        this_month_exp_total = this_month_exp_total + x.item_cost



    #Annual Expenses Records
    exp_this_year = SchoolExpenses.objects.filter(date_requested__year=current_year)
    this_year_exp_total = 0

    for x in exp_this_year:
        this_year_exp_total = this_year_exp_total + x.item_cost


    context={
        'school_expenses':school_expenses,
        'school_fees':school_fees,

        'total_expe':total_expe,
        'total_fee':total_fee,
        'total_asset': total_asset,

        'student_count':student_count,
        'teachers_count':teachers_count,
        'superuser_count':superuser_count,
        'accountant_count':accountant_count,

        'this_day_total': this_day_total,
        'this_month_total':this_month_total,
        'this_year_total':this_year_total,

        'this_day_exp_total': this_day_exp_total,
        'this_month_exp_total': this_month_exp_total,
        'this_year_exp_total': this_year_exp_total,
        }

    return render (request,'accounts/dashboard.html', context)

