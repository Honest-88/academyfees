import django_filters
from django_filters import CharFilter

from management.models import *


class student_filter(django_filters.FilterSet):
    student_number=CharFilter(field_name='student_number',lookup_expr='icontains',label="Student No")
    first_name=CharFilter(field_name='first_name',lookup_expr='icontains',label="First Name")
    last_name=CharFilter(field_name='last_name',lookup_expr='icontains',label="Last Name")
    grade=CharFilter(field_name='grade',lookup_expr='icontains',label="Grade")
    fees_status=CharFilter(field_name='fees_status',lookup_expr='icontains',label="Fees Status")
    class Meta:
          model=Student
          fields=(
         'student_number','first_name','last_name','grade',
         'fees_status','month','parent_phone','enrolement','gender',
          )

        
class staff_filter(django_filters.FilterSet):
    registration_number=CharFilter(field_name='registration_number',lookup_expr='icontains',label="ADM")
    first_name=CharFilter(field_name='first_name',lookup_expr='icontains',label="First Name")
    class Meta:
          model=Staff
          fields=(
         'first_name','role','registration_number',
         
          )