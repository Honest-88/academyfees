from django.db import models


Acquired_Through=[
    ('Cash','Cash'),
    ('Credit','Credit'),
    ('Donation','Donation')
]


class SchoolExpenses(models.Model):
    item_number = models.CharField(max_length=200, default='')
    item_name = models.CharField(max_length=200,blank=True, null=True)
    item_cost = models.IntegerField(blank=True, null=True) 
    requested_by = models.CharField(default='', max_length=100)
    payment_method = models.CharField(max_length=200,blank=True, null=True)
    permission_granted_by = models.CharField(max_length=100,blank=True, null=True)
    paid_by = models.CharField(max_length=300, blank=True, null=True) 
    reason = models.TextField(max_length=200,blank=True, null=True)
    date_requested = models.DateField(auto_now_add=True)
    

    class Meta:
        verbose_name = 'School Expenses'
        verbose_name_plural = 'School Expenses'

    
    def __str__(self):
       return str(self.item_number) + str(self.item_name)


# Create your models here.
class SchoolAssets(models.Model):
    asset_number = models.CharField(max_length=200, default='')
    asset_name = models.CharField(max_length=200, default='')
    number_of_assets = models.CharField(max_length=200, default='')
    asset_value = models.IntegerField(blank=True, null=True)
    acquired_through = models.CharField(choices=Acquired_Through, default='Cash', max_length=100)
    date_acqured = models.CharField(max_length=200, default='')
    date_added=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'School Asset'
        verbose_name_plural = 'School Assets'

    
    def __str__(self):
        return  str(self.asset_number) + ' ' + str(self.asset_name) +  ' asset_value '  + str(self.asset_value)