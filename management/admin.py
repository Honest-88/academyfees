from django.contrib import admin
from management.models import *
from import_export.admin import ImportExportModelAdmin


@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    search_fields=( 
        'student_number','first_name','last_name','month','grade','parent_phone',)
    list_filter=(
       'month','grade', 'fees_status','enrolement', 'gender','active',
    )
    list_display=(
   'student_number','first_name','last_name','month','grade', 'fees_status','parent_phone','enrolement', 'gender','active', 'date_added',
    )  


admin.site.register(Staff)
admin.site.register(Grade)
admin.site.register(Setting)
admin.site.register(AddmissionCharges)
admin.site.register(GradeDuration)
admin.site.register(Month)
admin.site.register(Audit)








 