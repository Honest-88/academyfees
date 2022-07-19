
from django.urls import path
from . import views

urlpatterns = [

path('register/student',views.register_student,name="register_student"),
path('search/student/',views.search_student,name="search_student_export"),
path('search/student/<str:grade>',views.search_student_one,name="search_student_one"),
path('list/student/',views.list_students,name="list_students"),
path('update/student/details/<str:pk>/',views.update_student,name="update_student"),
path('register/staff/',views.register_staff,name="register_staff"),
path('view/staff/',views.view_staff,name="view_staff"),
path('update/staff/<str:pk>/',views.update_staff,name="update_staff"),
path('export/staff/',views.export_staff,name="export_staff"),
path('configuration/one',views.configuration_one,name="configuration_one"),
path('configuration/final/<str:name>/<str:date_established>/<str:motto>/',views.configuration_two,name="configuration_two"),
path('student/export/<str:pk>/',views.single_student_export,name="single_student_export"),



]
