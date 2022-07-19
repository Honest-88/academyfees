from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User ,Profile
from .models import *


class StudentForm(forms.ModelForm):
   class Meta:
       model = Student
       fields=[
           'student_number','first_name','last_name','grade', 'fees_status', 'month','parent_phone','active','enrolement','gender','avatar'
       ]

class StaffForm(forms.ModelForm):
   class Meta:
       model = Staff
       fields=[
           'first_name','middle_name','last_name','last_name',
           'email','registration_number','role','phone',
           'active','avatar'
       ]
