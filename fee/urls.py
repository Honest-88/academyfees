
from django.urls import path
from .import views


urlpatterns = [

path('fee/search/student/',views.search_student,name="search_student"),
path('pay/fee/student/<path:registration_number>/',views.pay_fee,name="pay_fee"),
path('view/all/fee/',views.view_all_fee,name="view_all_fee"),
path('transaction/all/fee/',views.export_transactions,name="export_transactions"),
path('print/receipt/<str:pk>/',views.export_one,name="export_one"),

path('show/edit/form',views.show_payment_edit_form,name="show_payment_edit_form"),
path('edit/receipt/payment/<str:pk>/',views.edit_payment,name="edit_payment"),


]