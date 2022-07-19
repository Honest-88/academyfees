from django.urls import path
from . import views

urlpatterns = [

path('list/expenses/',views.list_expenses,name="list_expenses"),
path('add/expense',views.add_expense,name="add_expense"),
path('add/asset',views.add_asset,name="add_asset"),
path('list/assets/',views.list_assets,name="list_assets"),


]
