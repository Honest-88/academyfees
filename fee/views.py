from multiprocessing.dummy import current_process
from django.shortcuts import render
# Create your views here.
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
from management.models import *
from .models import *
from .filters import payment_filter
from management.filters import student_filter
from .forms import payment_edit_form


@login_required(login_url='loginuser')
def search_student(request):
    if request.user.is_superuser or request.user.is_accountant or request.user.is_registrar:
        student_obj=Student.objects.all()
        form=student_filter(request.GET,queryset=student_obj)
        student_obj=form.qs
        
        student_number=request.POST.get('student_number')
        # using name
        student_name=request.POST.get('student_name')
        print(student_name)

        # first_name       
        student_exist=Student.objects.filter(student_number=student_number)
        if not student_exist:
            pass
        else:
            return redirect('pay_fee',student_number)               
        return render (request,'fee/search_student.html',{'student_number':student_number,'form':form,'student_exist':student_exist,'student_obj':student_obj})
    else:
        return redirect('dashboard')

@login_required(login_url='loginuser')
def pay_fee(request,registration_number):
    if request.user.is_superuser :
        #request data
        dynamic_amount=0
        payment_method=''
        code=''
        whopaid=''
        amount=0
        if  request.method=="POST":
            amount=request.POST.get('amount')
            code=request.POST.get('code')
            whopaid=request.POST.get('whopaid')
            payment_method=request.POST.get('p')
        #using a name from search here can be tricky because we are matching the student with exactly that number
        # its not a filter , using a name could now change the flow where by we can search by name nd then list all the potential
        # student matching that name then select the student we want and pic the admission number from there    
        student_obj=Student.objects.filter(student_number=registration_number)
        single_student_obj=Student.objects.filter(student_number=registration_number).first()
        student_name=str(single_student_obj.first_name) + str(single_student_obj.last_name)
        year=datetime.today().year
        #-----------------------------
        grade_=single_student_obj.grade
        month=single_student_obj.month
        grade_id=single_student_obj.grade.id
        month_id=single_student_obj.month.id
        print('month',month_id)
        grade_obj=Grade.objects.filter(id=grade_id).first()
        this_student_money_expected_as_from_grade=FeesParticular.objects.filter(grade=grade_id).first()

        has_ever_paid=Payment.objects.filter(student_number=registration_number)
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # this code is somehow independent to show money expected in pay fee page 
        _grade=(single_student_obj.grade)
        _grade_id=(single_student_obj.grade.id)
        payment_obj_independent=Payment.objects.filter(student_number=registration_number)
        max_id=0
        for x in payment_obj_independent:
            if x.id > max_id:
                max_id=x.id
        independent_recent_pay=Payment.objects.filter(id=max_id).first()
        if not has_ever_paid:
            dynamic_amount=grade_obj.amount
        else:
            if grade_obj==independent_recent_pay.grade:
                dynamic_amount=independent_recent_pay.current_arrears
            else:
                dynamic_amount=independent_recent_pay.current_arrears + grade_obj.amount
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        if not has_ever_paid :
            if request.method=='POST':
                previous_arrears=this_student_money_expected_as_from_grade.amount_payable
                current_arrears= previous_arrears - int(amount)
                Payment.objects.create(
                    student_number=registration_number,
                        month=month,
                        previous_arrears=previous_arrears,
                        amount_paid=amount,
                        payment_method=payment_method,
                        reference_code=code,
                        current_arrears=current_arrears,
                        grade=grade_obj,
                        student_name=student_name,
                        paid_by=whopaid,
                        year=year)
                return redirect('/view/all/fee/')
        else:
            if request.method=='POST':
                payment_obj=Payment.objects.filter(student_number=registration_number)
                max_id=0
                for x in payment_obj:
                    if x.id > max_id:
                        max_id=x.id
                recent_pay=Payment.objects.filter(id=max_id).first()
                if recent_pay:
                    previous_arrears=recent_pay.current_arrears
                    current_arrears= previous_arrears - int(amount)
                    # check if grade has changed
                    _grade=(single_student_obj.grade)
                    _grade_id=(single_student_obj.grade.id)
                    print(grade_obj)
                    print(recent_pay.grade)
                    # grade still the same so deduct from pravious latest record 
                    if (grade_obj==recent_pay.grade):
                        Payment.objects.create(
                            student_number=registration_number,
                            month=month,
                            previous_arrears=previous_arrears,
                            amount_paid=amount,
                            payment_method=payment_method,
                            reference_code=code,
                            current_arrears=current_arrears,
                            grade=grade_obj,
                            student_name=student_name,
                            paid_by=whopaid,
                            year=year)
                    else:
                        __grade_obj=Grade.objects.filter(grade_name=_grade).first()
                        # now the grade is changed 
                        Payment.objects.create(
                            student_number=registration_number,
                            month=month,
                            previous_arrears=previous_arrears + __grade_obj.amount,
                            amount_paid=amount,
                            payment_method=payment_method,
                            reference_code=code,
                            current_arrears=(previous_arrears + __grade_obj.amount)-int(amount),
                            grade=grade_obj,
                            student_name=student_name,
                            paid_by=whopaid,
                            year=year)
                               
                    return redirect('/view/all/fee/')
# redirect accordingly from here 
        return render (request,'fee/pay_fee.html',{'dynamic_amount':dynamic_amount,'registration_number':registration_number,'this_student_money_expected_as_from_grade':this_student_money_expected_as_from_grade,'student_obj':student_obj,'grade_':grade_,'month':month,'registration_number':registration_number})
    else:
        return redirect('dashboard')


@login_required(login_url='loginuser')
def view_all_fee(request):
    if request.user.is_superuser:
        fee=Payment.objects.all().order_by('id')  
        form= payment_filter(request.POST,queryset=fee)
        fee=form.qs
        count=fee.count()
        return render (request,'fee/view_all_fee.html',{'fee':fee,'form':form,'count':count})
    else:
        return redirect('dashboard')


@login_required(login_url='loginuser')
def export_transactions(request):
    if request.user.is_superuser:
        get_date=datetime.now()
        u=request.user
        fee=Payment.objects.all().order_by('-date_added')
        count=fee.count()
        # Rendered
        html_string = render_to_string('fee/pdf/export_transactions.html', {'get_date':get_date,'fee':fee,'u':u,'count':count  })
        html = HTML(string=html_string,base_url=request.build_absolute_uri())
        result = html.write_pdf()
        # Creating http response
        response = HttpResponse(content_type='application/pdf;')
        response['Content-Disposition'] = 'inline; all transactions.pdf'
        response['Content-Transfer-Encoding'] = 'binary'
        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output = open(output.name, 'rb')
            response.write(output.read())
    else:
        return redirect('dashboad')

    return response


@login_required(login_url='loginuser')
def export_one(request,pk):
    if request.user.is_superuser:
        i=Payment.objects.get(id=pk)
        get_date=datetime.now()
        u=request.user
        # Rendered
        html_string = render_to_string('fee/pdf/export_one.html', {'get_date':get_date,'i':i,'u':u  })
        html = HTML(string=html_string,base_url=request.build_absolute_uri())
        result = html.write_pdf()
        # Creating http response
        response = HttpResponse(content_type='application/pdf;')
        response['Content-Disposition'] = 'inline;receipt.pdf'
        response['Content-Transfer-Encoding'] = 'binary'
        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output = open(output.name, 'rb')
            response.write(output.read())
    else:
        return redirect('dashboad')

    return response

@login_required(login_url='loginuser')
def show_payment_edit_form(request):
    if request.user.is_superuser:
       form=payment_edit_form()
    else:
        return redirect("dashboard")

    return render (request,'fee/show_payment_edit_form.html',{'form':form})


@login_required(login_url='loginuser')
def edit_payment(request,pk):
    if request.user.is_superuser:
       i=Payment.objects.get(id=pk)
       form=payment_edit_form(instance=i)
       if request.method=="POST":
           form=payment_edit_form(request.POST, instance=i)
           if form.is_valid():
               form.save()
               messages.info(request,'Transaction was updated ')
               return redirect('view_all_fee')

    else:
        return redirect("dashboard")

    return render (request,'fee/show_payment_edit_form.html',{'form':form})


@login_required(login_url='loginuser')
def delete_transaction(request,pk):
    if request.user.is_superuser:
        i=Payment.objects.get(id=pk)
        if request.method=="POST":
            i.delete()
            messages.info(request,'Transaction deleted succesfully')
            return redirect('View_all_students')
    else:
        return redirect("dashboard")

    return render (request,'accounts/delete_transaction.html',{'student':student})




    
