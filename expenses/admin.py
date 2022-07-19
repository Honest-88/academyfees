from django.contrib import admin

from expenses.models import *
from import_export.admin import ImportExportModelAdmin


@admin.register(SchoolExpenses)
class SchoolExpensesAdmin(ImportExportModelAdmin):
    search_fields=( 
        'item_name','requested_by', 'permission_granted_by',)
    list_filter=(
       'item_name','item_cost', 'requested_by','payment_method','permission_granted_by','date_requested',
    )
    list_display=(
   'item_number','item_name','item_cost', 'requested_by','payment_method','permission_granted_by', 'paid_by','reason','date_requested',
    ) 


@admin.register(SchoolAssets)
class SchoolAssetsAdmin(ImportExportModelAdmin):
    search_fields=( 
        'asset_number','asset_name',)
    list_filter=(
       'asset_number','asset_name', 'acquired_through','asset_value','date_acqured',
    )
    list_display=(
   'asset_number','asset_name','number_of_assets', 'asset_value','acquired_through','date_acqured', 'date_added',
    )  




