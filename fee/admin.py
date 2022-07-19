from django.contrib import admin
from . models import *

from import_export.admin import ImportExportModelAdmin
# Register your models here.



@admin.register(Payment)
class PaymentAdmin(ImportExportModelAdmin):
    search_fields=( 
        'student_number','student_name','month',
'previous_arrears','amount_paid','current_arrears',
'payment_method','reference_code','grade','date_added',
'year','paid_by')
    list_filter=(
        'student_number','student_name','month','fees_status',
'previous_arrears','amount_paid','current_arrears',
'payment_method','reference_code','grade','date_added',
'year','paid_by'
    )
    list_display=(
    'student_number','student_name','month','fees_status',
'previous_arrears','amount_paid','current_arrears',
'payment_method','reference_code','grade','date_added',
'year','paid_by'
    )  


@admin.register(FeesParticular)
class FeesParticularAdmin(ImportExportModelAdmin):
    search_fields=('grade','month','amount_payable','year','date_added')
    list_filter=('grade','month','amount_payable','year','date_added')
    list_display=(
     'grade','month','amount_payable','year','date_added'
    ) 

@admin.register(AuditTrailFinance)
class AuditTrailFinanceAdmin(ImportExportModelAdmin):
    search_fields=()
    list_filter=('user','action','item','date','page','description','date_added')
    list_display=(
     'user','action','item','date','page','description','date_added'
    )   
    def has_delete_permission(self, request, obj=None):
            # Disable delete
        return False
    def has_add_permission(self, request):
        return False
    def save_model(self, request, obj, form, change):
            #Return nothing to make sure user can't update any data
        pass
    def get_readonly_fields(self, request, obj=None):
        if obj:
          return ['user']
        else:
            return []