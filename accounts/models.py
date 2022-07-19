from __future__ import unicode_literals

from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from accounts.managers import UserManager
from django.conf import settings


from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField




from django.db import models


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), default='', unique=True)
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff'), default=True)
    is_admin=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    is_accountant=models.BooleanField(default=False)
    is_teacher=models.BooleanField(default=False)
    is_student=models.BooleanField(default=False)

    phone=models.CharField(max_length=200)
    registration_number=models.CharField(unique=True,max_length=50)

    objects = UserManager()
    USERNAME_FIELD = 'registration_number'
    REQUIRED_FIELDS = ['email','first_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)
        
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture=models.ImageField(upload_to='pics',default="np_pic.png")
    studied_at=models.CharField(max_length=200,blank=True,null=True)
    county=models.CharField(max_length=200,blank=True,null=True)
    location=models.CharField(max_length=200,blank=True,null=True)
    my_profile=models.CharField(max_length=200,blank=True,null=True)
    phone=models.CharField(max_length=200,blank=True,null=True)
    occupation=models.CharField(max_length=200,blank=True,null=True)
    education=models.CharField(max_length=200,blank=True,null=True)
    skills=models.CharField(max_length=200,blank=True,null=True)
    notes=models.CharField(max_length=200,blank=True,null=True)
    country =CountryField(blank=True,null=True)

    def __str__(self):
        return str(self.user.email)
    @receiver(post_save, sender=User)
    def create_user_p(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
    @receiver(post_save, sender=User)
    def save_user_p(sender, instance, **kwargs):
        instance.profile.save()


class TermsAndConditions(models.Model):
    term=models.TextField(max_length=500)
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  str(self.term)
