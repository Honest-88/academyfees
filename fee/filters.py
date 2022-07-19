import django_filters
from django_filters import CharFilter

from .models import *


class payment_filter(django_filters.FilterSet):
    student_number=CharFilter(field_name='student_number',lookup_expr='icontains',label="Student No")
    first_name=CharFilter(field_name='first_name',lookup_expr='icontains',label="First Name")
    last_name=CharFilter(field_name='last_name',lookup_expr='icontains',label="Last Name")
    grade=CharFilter(field_name='grade',lookup_expr='icontains',label="Grade")

    class Meta:
          model=Payment
          fields=(
     'student_number','month','first_name','first_name',
'payment_method','reference_code','grade','id',
'year'
          )
