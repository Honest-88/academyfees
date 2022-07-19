# from typing_extensions import Required
from django.db import models
from accounts.models import User
from django.db.models.fields import IntegerField


ROLES_CHOICES=[
    ('superuser','superuser'),
    ('acountant','acountant'),
    ('teacher','teacher'),
    
   
]

Fees_Status=[
    ('CLEARED','CLEARED'),
    ('ON ARRANGEMENT','ON ARRANGEMENT'),
    ('NOT PAID','NOT PAID')
]

Gender_CHOICES=[
    ('male','male'),
    ('female','female'), 
]


enrolement_CHOICES=[
    ('jan','jan'),
    ('feb','feb'),
    ('march','march'),
    ('april','april'),
     ('may','may'),
      ('june','june'),
       ('july','july'),
        ('august','august'),
         ('sep','sep'),
         ('oct','oct'),
          ('nov','nov'),
           ('dec','dec'),
        
]


class GradeDuration(models.Model):
    duration=models.CharField(max_length=500,unique=True)
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  str(self.duration)
class Month(models.Model):
    month=models.CharField(max_length=500,unique=True)
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  str(self.month)

class Grade(models.Model):
    grade_name=models.CharField(max_length=500 ,unique=True)
    duration=models.ForeignKey(GradeDuration, on_delete=models.CASCADE)
    month=models.ForeignKey(Month, on_delete=models.CASCADE)
    amount=models.IntegerField()
    requirement=models.TextField(max_length=1000,blank=True, null=True)
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  str(self.grade_name)

class Setting(models.Model):
    school_name=models.CharField(max_length=500)
    date_established=models.DateField(auto_created=False)
    motto=models.CharField(max_length=50)
    location=models.CharField(max_length=50)
    address=models.CharField(max_length=50)
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  str(self.school_name)


class Student(models.Model):
    student_number=models.CharField(max_length=200, default='')
    first_name=models.CharField(max_length=500)
    last_name=models.CharField(max_length=500)
    grade=models.ForeignKey(Grade, default='Grade R', on_delete=models.CASCADE)
    # fee status served better by bo0lean , but i wont change it 
    fees_status=models.CharField(choices=Fees_Status, default='NOT PAID', max_length=100)
    month=models.ForeignKey(Month, on_delete=models.CASCADE)
    parent_phone=models.CharField(max_length=50,blank=True,null=True)
    enrolement=models.CharField(choices=enrolement_CHOICES, default='Jan', max_length=100)
    gender=models.CharField(choices=Gender_CHOICES, max_length=50)
    active=models.BooleanField(default=True)
    avatar=models.ImageField(upload_to='images',blank=True, null=True)
    date_added=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return  str(self.first_name) + ' ' + str(self.last_name) +  ' student_number '  + str(self.student_number) 

class Staff(models.Model):
    first_name=models.CharField(max_length=500)
    middle_name=models.CharField(max_length=500)
    last_name=models.CharField(max_length=500)
    email=models.EmailField(max_length=254,unique=True)
    registration_number=models.CharField(max_length=50,unique=True)
    role=models.CharField(choices=ROLES_CHOICES, max_length=50)
    active=models.BooleanField(default=True)
    phone=models.CharField( max_length=50 ,blank=True, null=True)
    avatar=models.ImageField(upload_to='images',blank=True, null=True)
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  str(self.first_name) + ' ' + str(self.last_name) +  ' registration number '  + str(self.registration_number)

class AddmissionCharges(models.Model):
    particular_name=models.CharField(max_length=500)
    amount=models.IntegerField()
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  str(self.particular_name) 


class Audit(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    action=models.CharField(max_length=50)
    object=models.CharField(max_length=50)
    description=models.TextField(max_length=50)
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  str(self.user) + str(self.action) + ' ' + ' ' + 'time ' + str(self.date_added)