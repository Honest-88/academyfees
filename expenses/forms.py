from django import forms
from accounts.models import User ,Profile
from .models import *


class AssetForm(forms.ModelForm):
   class Meta:
       model = SchoolAssets
       fields=[
           'asset_number','asset_name','number_of_assets','asset_value','acquired_through','date_acqured',
       ]

class ExpenseForm(forms.ModelForm):
   class Meta:
       model = SchoolExpenses
       fields=[
           'item_number','item_name','item_cost','requested_by','payment_method','permission_granted_by','paid_by','reason',
       ]

