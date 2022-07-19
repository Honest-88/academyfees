from django.contrib import admin
from accounts.models import User, Profile,TermsAndConditions
from import_export.admin import ImportExportModelAdmin



@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    search_fields=('email',)
    list_filter=('email','last_name','first_name','date_joined','is_active')
    list_display=(
        'email','first_name','last_name','date_joined','is_active','is_staff','is_admin','is_superuser','is_accountant','is_teacher','is_student'
    )      


class ProfileAdmin(admin.ModelAdmin):
    list_filter=('user','studied_at','county','location','phone')
    search_fields=('user',)
    list_display=(
        'user','picture','studied_at','county','location','my_profile','phone','occupation','education','skills','notes','country'
    ) 
admin.site.register(Profile,ProfileAdmin)


@admin.register(TermsAndConditions)
class TermsAndConditionsAdmin(ImportExportModelAdmin):
    list_filter=('term','date_added')
    search_fields=('term','date_added')
    list_display=(
       'term','date_added'
    ) 
