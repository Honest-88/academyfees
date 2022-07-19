from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

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
from .forms import *
from expenses.models import *
from management.models import *
from accounts.models import User

#password change 

from django.shortcuts import render
from django.contrib.auth.hashers import make_password

@login_required(login_url='loginuser')
def list_expenses(request):
    if request.user.is_superuser or request.user.is_accountant or request.user.is_registrar:
        school_expenses=SchoolExpenses.objects.all().order_by('-date_requested')
       # AssetForm=school_assets(request.GET,school_assets=school_assets)
       # school_assets=AssetForm
        #count=school_assets.count()
        # this how you do the total 
        total_expe=0
        for x in school_expenses:
            total_expe= total_expe + x.item_cost

        context={
        'school_expenses':school_expenses,
        'total_expe':total_expe,
        #'count':count,
        #'AssetForm':AssetForm
        }
        return render (request,'assets/expenses.html',context)
    else:
        return redirect('dashboard')

@login_required(login_url='loginuser')
def add_expense(request):
    if request.user.is_superuser or request.user.is_accountant or request.user.is_registrar:
        form=ExpenseForm()
        if request.method=="POST":
            form=ExpenseForm(request.POST,request.FILES)
            if form.is_valid():
                form.save()
                item_number=form.cleaned_data.get('item_number')
                item_name=form.cleaned_data.get('item_name')
                item_cost=form.cleaned_data.get('item_cost')
                requested_by=form.cleaned_data.get('requested_by')
                payment_method=form.cleaned_data.get('payment_method')
                permission_granted_by=form.cleaned_data.get('permission_granted_by')
                paid_by=form.cleaned_data.get('paid_by')
                reason=form.cleaned_data.get('reason')

                registration_number_exist=User.objects.filter(registration_number=item_name)
                user=request.user
                action='Add Expense'
                date=datetime.now()
                page=request.META.get('HTTP_REFERER')
                description= ("User {} registered {} On Page {} ".format(user, item_name, page))
                obj=Audit.objects.create(
                    user=user,
                    action=action,
                    object=item_name,
                    description=description,
                
                    )
                obj.save()
                '''
                if not registration_number_exist:
                    User.objects.create(registration_number=student_no,password=make_password('banking001'),is_student=True,first_name=first_name,last_name=last_name)
                    print('user created')
                else:
                    pass
                '''
                messages.info(request,f'SchoolExpenses {item_name} A New Expenses {item_name} ware registerd successfully  ')

        context={
            'form':form
        }
        return render (request,'assets/add_expense.html', context)
    else:
        return redirect('dashboard')


@login_required(login_url='loginuser')
def add_asset(request):
    if request.user.is_superuser or request.user.is_accountant or request.user.is_registrar:
        form=AssetForm()
        if request.method=="POST":
            form=AssetForm(request.POST,request.FILES)
            if form.is_valid():
                form.save()
                asset_number=form.cleaned_data.get('asset_number')
                asset_name=form.cleaned_data.get('asset_name')
                number_of_assets=form.cleaned_data.get('number_of_assets')
                asset_value=form.cleaned_data.get('asset_value')
                acquired_through=form.cleaned_data.get('acquired_through')
                date_acqured=form.cleaned_data.get('date_acqured')

                registration_number_exist=User.objects.filter(registration_number=asset_number)
                user=request.user
                action='Add Aseet'
                date=datetime.now()
                page=request.META.get('HTTP_REFERER')
                description= ("User {} registered {} On Page {} ".format(user, asset_number, page))
                obj=Audit.objects.create(
                    user=user,
                    action=action,
                    object=asset_number,
                    description=description,
                
                    )
                obj.save()
                '''
                if not registration_number_exist:
                    User.objects.create(registration_number=student_no,password=make_password('banking001'),is_student=True,first_name=first_name,last_name=last_name)
                    print('user created')
                else:
                    pass
                '''
                messages.info(request,f'SchoolAssets {asset_name} A New Asset {asset_number} was registerd successfully  ')

        context={
            'form':form
        }
        return render (request,'assets/add_asset.html', context)
    else:
        return redirect('dashboard')


@login_required(login_url='loginuser')
def list_assets(request):
    if request.user.is_superuser or request.user.is_accountant or request.user.is_registrar:
        school_assets=SchoolAssets.objects.all().order_by('-date_added')
       # AssetForm=school_assets(request.GET,school_assets=school_assets)
       # school_assets=AssetForm
        #count=school_assets.count()
        total_asset=0
        for x in school_assets:
            total_asset= total_asset + x.asset_value

        context={
        'school_assets':school_assets,
        'total_asset':total_asset,
        }
        return render (request,'assets/asset_list.html',context)
    else:
        return redirect('dashboard')


