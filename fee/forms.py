

from django import forms
from .models import Payment


class payment_edit_form(forms.ModelForm):
   class Meta:
       model = Payment
       fields=[
        'student_number','student_name','month','fees_status',
        'previous_arrears','amount_paid','current_arrears',
        'payment_method','reference_code','grade',
        'year','paid_by'
       ]

