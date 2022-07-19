from django.db import models
from management.models import *


Fees_Status=[
    ('CLEARED','CLEARED'),
    ('ON ARRANGEMENT','ON ARRANGEMENT'),
    ('NOT PAID','NOT PAID')
]

PAYMENT_METHOD_CHOICES=(
    ('Bank','Bank'),
    ('Cash','Cash'),
    ('Other','Other'),
)

class FeesParticular(models.Model):
    grade = models.ForeignKey(Grade, default='Grade R', on_delete=models.CASCADE)
    month = models.ForeignKey(Month, on_delete=models.CASCADE)
    amount_payable=models.IntegerField(default=0)
    year=models.IntegerField(blank=True, null=True)
    date_added = models.DateField(auto_now_add=True)
    def __str__(self):
       return  str(self.amount_payable)

class Payment(models.Model):
    student_number=models.CharField(max_length=200, default='')
    student_name=models.CharField(max_length=200,blank=True, null=True)
    grade = models.ForeignKey(Grade,default='Grade R', on_delete=models.CASCADE)
    month = models.ForeignKey(Month, on_delete=models.CASCADE)
    previous_arrears=models.IntegerField()
    amount_paid=models.IntegerField(blank=True, null=True)
    current_arrears=models.IntegerField()
    fees_status=models.CharField(choices=Fees_Status, default='NOT PAID', max_length=100)
    payment_method=models.CharField(max_length=200,blank=True, null=True)
    reference_code=models.CharField(max_length=100,blank=True, null=True)
    date_added = models.DateField(auto_now_add=True)
    year=models.CharField(max_length=300, blank=True, null=True)
    paid_by=models.CharField(max_length=300, blank=True, null=True)
    def __str__(self):
       return str(self.grade) + str(self.month)


class AuditTrailFinance(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    action=models.CharField(max_length=50)
    item=models.TextField(max_length=300)
    date=models.CharField(max_length=400)
    page=models.CharField(max_length=1000)
    description=models.TextField(max_length=1000)
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  str(self.user)
    class Meta:
            verbose_name = ('Audit Trail')
            verbose_name_plural = ('Audit Trail ' )