
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('dd/dd/s',views.index,name="index"),
    path('register/',views.registeruser,name="registeruser"),
    path('',views.loginuser,name="loginuser"),
    path('dashboard/', views.dashboard,name="dashboard"),
    path('logoutuser/', views.logoutuser,name="logoutuser"),
    path('profile/', views.profile,name="profile"),
    path('viewprofile/', views.viewprofile,name="viewprofile"),
    path('updateprofile/<str:pk>/', views.updateprofile,name="updateprofile"),
    path('change_password/', views.change_password,name="change_password"),
    path('term_and_condations/', views.term_and_condations_view,name="term_and_condations"),
 

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name = "accounts/reset_password.html"), name ='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = "accounts/password_reset_sent.html"), name ='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name = "accounts/password_reset_form.html"), name ='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "accounts/password_reset_done.html"), name ='password_reset_complete')
  
]
