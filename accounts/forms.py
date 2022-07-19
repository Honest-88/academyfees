from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User ,Profile

class UserRegistrationForm(UserCreationForm):
   email=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'xyz@email.com'}))
   class Meta:
       model = User
       fields=[
           'email','first_name','phone','password1','password2'
       ]

class ProfileForm(forms.ModelForm):
   class Meta:
       model = Profile
       fields=[
           'picture','studied_at','county','location','my_profile','phone','country','occupation','skills','notes'
       ]

