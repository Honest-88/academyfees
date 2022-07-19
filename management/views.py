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
from accounts.models import User
from .filters import student_filter,staff_filter
#password change 

from django.shortcuts import render
from django.contrib.auth.hashers import make_password
# Create your views here.


@login_required(login_url='loginuser')
def register_student(request):
    if request.user.is_superuser or request.user.is_accountant or request.user.is_registrar:
        form=StudentForm()
        if request.method=="POST":
            form=StudentForm(request.POST,request.FILES)
            if form.is_valid():
                form.save()
                student_no=form.cleaned_data.get('student_number')
                name=form.cleaned_data.get('first_name')
                first_name=form.cleaned_data.get('first_name')
                last_name=form.cleaned_data.get('last_name')
                middle_name=form.cleaned_data.get('middle_name')
                registration_number_exist=User.objects.filter(registration_number=student_no)
                user=request.user
                action='Student Registration'
                date=datetime.now()
                page=request.META.get('HTTP_REFERER')
                description= ("User {} registered {} On Page {} ".format(user, student_no, page))
                obj=Audit.objects.create(
                    user=user,
                    action=action,
                    object=student_no,
                    description=description,
                
                    )
                obj.save()
                # if not registration_number_exist:
                #     User.objects.create(registration_number=student_no,password=make_password('123456789'),is_student=True,first_name=first_name,last_name=last_name)
                #     print('user created')
                # else:
                #     pass
               
                messages.info(request,f'student {name} student number {student_no}  registerd successfully  ')

        context={
            'form':form
        }
        return render (request,'management/register_student.html',context)
    else:
        return redirect('dashboard')

@login_required(login_url='loginuser')
def search_student(request):
    if request.user.is_superuser or request.user.is_accountant or request.user.is_registrar:
        grades=Grade.objects.all()
        if request.method=="POST":
            grade=request.POST.get('grade')
            return redirect('search_student_one',grade)
            
        context={
        'grades':grades
        }
        return render (request,'management/seach_student_one.html',context)
    else:
        return redirect('dashboard')


@login_required(login_url='loginuser')
def search_student_one(request, grade):
    if request.user.is_superuser or request.user.is_accountant or request.user.is_registrar:
        grade=grade
        grades_all=Grade.objects.filter(id=grade)
        for x in grades_all:
            get_name_of_grade=x.grade_name
        print('grade', grade)
        get_date=datetime.now()
        u=str(request.user.first_name )+str(request.user.first_name )
        student=Student.objects.filter(grade=grade,active=True)
        count=student.count()
        # Rendered
        html_string = render_to_string('management/pdf/pdf_students.html', {'get_date':get_date,'student':student,'u':u,'count':count , 'get_name_of_grade':get_name_of_grade})
        html = HTML(string=html_string,base_url=request.build_absolute_uri())
        result = html.write_pdf()
        # Creating http response
        response = HttpResponse(content_type='application/pdf;')
        response['Content-Disposition'] = 'inline; students.pdf'
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
def list_students(request):
    if request.user.is_superuser or request.user.is_accountant or request.user.is_registrar:
        student=Student.objects.all().order_by('-date_added')
        form=student_filter(request.GET,queryset=student)
        student=form.qs
        count=student.count()

        context={
        'student':student,
        'count':count,
        'form':form,       
        }
        return render (request,'management/list_students.html',context)
    else:
        return redirect('dashboard')



@login_required(login_url='loginuser')
def update_student(request,pk):
    if request.user.is_superuser or request.user.is_accountant or request.user.is_registrar:
        i=Student.objects.get(id=pk)
        form=StudentForm(instance=i)
        if request.method=="POST":
            form=StudentForm(request.POST,request.FILES,instance=i)
            if form.is_valid():
                form.save()
                # student_number_exist=User.objects.filter(student_number=student_no)
                # name=form.cleaned_data.get('first_name')
                # first_name=form.cleaned_data.get('first_name')
                # last_name=form.cleaned_data.get('last_name')
                # middle_name=form.cleaned_data.get('middle_name')
                # active=form.cleaned_data.get('active')

                # user=request.user
                # action='Student update'
                # date=datetime.now()
                # page=request.META.get('HTTP_REFERER')
                # description= ("User {} upadated {} On Page {} ".format(user, student_no, page))
                # obj=Audit.objects.create(
                #     user=user,
                #     action=action,
                #     object=student_no,
                #     description=description,
                
                #     )
                # obj.save()
                # User.objects.filter(student=student_no).update(is_active=active)
                
              
                messages.info(request,'student   updated successfully  ')
                return redirect('list_students')

        context={
            'form':form
        }
        return render (request,'management/register_student.html',context)
    else:
        return redirect('dashboard')




@login_required(login_url='loginuser')
def register_staff(request):
    if request.user.is_superuser :
        form=StaffForm()
        if request.method=="POST":
            form=StaffForm(request.POST)
            if form.is_valid():
                form.save()
                email=form.cleaned_data.get('email')
                name=form.cleaned_data.get('first_name')
                regno=form.cleaned_data.get('registration_number')
                role=form.cleaned_data.get('role')
                user=request.user
                action='staff registration'
                date=datetime.now()
                page=request.META.get('HTTP_REFERER')
                description= ("User {} registerd {} ,staff number {} On Page {} ".format(user, role, regno, page))
                obj=Audit.objects.create(
                    user=user,
                    action=action,
                    object=regno,
                    description=description,
                
                    )
                obj.save()

                email_exist=User.objects.filter(email=email)
                reg_exist=User.objects.filter(registration_number=regno)
                if not email_exist or regno:
                    if role=='superuser':
                        User.objects.create(email=email,registration_number=regno,is_superuser=True,first_name=name,password=make_password('banking001'))
                    elif role=='acountant':
                         User.objects.create(email=email,registration_number=regno,is_accountant=True,first_name=name,password=make_password('banking001'))
                    else:
                         User.objects.create(email=email,registration_number=regno,is_teacher=True,first_name=name,password=make_password('banking001'))
                else:
                    pass
                messages.info(request,f'staff {name} registration number {regno} , email {email} registred successfully  ')

        context={
                'form':form
        }
        return render (request,'management/register_staff.html',context)
    else:
        return redirect('dashboard')




@login_required(login_url='loginuser')
def view_staff(request):
    if request.user.is_superuser or request.user.is_accountant or request.user.is_registrar:
        staff=Staff.objects.all()
        form=staff_filter(request.GET,queryset=staff)
        staff=form.qs
        count=staff.count()

            
        context={
        'staff':staff,
        'count':count,
        'form':form
        }
        return render (request,'management/view_staff.html',context)
    else:
        return redirect('dashboard')


@login_required(login_url='loginuser')
def update_staff(request,pk):
    if request.user.is_superuser :
        i=Staff.objects.get(id=pk)
        form=StaffForm(instance=i)
        if request.method=="POST":
            form=StaffForm(request.POST,request.FILES,instance=i)
            if form.is_valid():
                form.save()
                email=form.cleaned_data.get('email')
                name=form.cleaned_data.get('first_name')
                regno=form.cleaned_data.get('registration_number')
                role=form.cleaned_data.get('role')
                user=request.user
                action='staff update'
                date=datetime.now()
                page=request.META.get('HTTP_REFERER')
                description= ("User {} updated {} ,staff number {} On Page {} ".format(user, role, regno, page))
                obj=Audit.objects.create(
                    user=user,
                    action=action,
                    object=regno,
                    description=description,
                
                    )
                obj.save()

                email_exist=User.objects.filter(email=email)
                reg_exist=User.objects.filter(registration_number=regno)
                messages.info(request,f'staff {name} registration number {regno} , email {email} updated successfully  ')
                return redirect('view_staff')

        context={
                'form':form
        }
        return render (request,'management/register_staff.html',context)
    else:
        return redirect('dashboard')


@login_required(login_url='loginuser')
def export_staff(request):
    if request.user.is_superuser:
        get_date=datetime.now()
        u=request.user
        teacher=Staff.objects.all()
        count=teacher.count()
        # Rendered
        html_string = render_to_string('management/pdf/export_staff.html', {'get_date':get_date,'export_staff':export_staff,'u':u,'count':count ,'teacher':teacher })
        html = HTML(string=html_string,base_url=request.build_absolute_uri())
        result = html.write_pdf()
        # Creating http response
        response = HttpResponse(content_type='application/pdf;')
        response['Content-Disposition'] = 'inline; staffs.pdf'
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
def configuration_one(request):
    if request.user.is_superuser:
        if request.method=="POST":
           name=request.POST.get('name')
           date_established=request.POST.get('date_established')
           motto=request.POST.get('motto')
           print(name,date_established,motto,'one')
           return redirect('configuration_two',name,date_established,motto)
            
        context={
            
                }
        return render (request,'management/configuration_one.html',context)
    else:
        return redirect('dashboard')
    


@login_required(login_url='loginuser')
def configuration_two(request,name,date_established,motto):
    if request.user.is_superuser:
        if request.method=="POST":
           name=name
           date_established=date_established
           motto=motto
           print(name,date_established,motto,'onejjjjjjjjjjjjjjjjjjjjjjjjjjj')
           if request.method=="POST":
            location=request.POST.get('location')
            address=request.POST.get('address')
            print(location,address,'wooooooooooooooooooooooooooooooooo')
            settings=Setting.objects.all().count()
            if settings == 0 :
                Setting.objects.create(
                    school_name=name,
                    date_established=date_established,
                    motto=motto,
                    location=location,
                    address=address
                )
            else:
                return redirect('dashboard')
            return redirect('dashboard')
           return redirect('configuration_two',name,date_established,motto)
            
        context={
            
                }
        return render (request,'management/configuration_two.html',context)
    else:
        return redirect('dashboard')




@login_required(login_url='loginuser')
def single_student_export(request,pk):
    if request.user.is_superuser:
        i=Student.objects.get(id=pk)
        get_date=datetime.now()
        u=request.user
        # Rendered
        html_string = render_to_string('management/pdf/single_student_export.html', {'get_date':get_date,'i':i,'u':u ,'i':i })
        html = HTML(string=html_string,base_url=request.build_absolute_uri())
        result = html.write_pdf()
        # Creating http response
        response = HttpResponse(content_type='application/pdf;')
        response['Content-Disposition'] = 'inline;student.pdf'
        response['Content-Transfer-Encoding'] = 'binary'
        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output = open(output.name, 'rb')
            response.write(output.read())
    else:
        return redirect('dashboad')

    return response