from django.db import models

# from __future__ import unicode_literals
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, UserManager
from django.core.validators import RegexValidator
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
# from blissemaths.utils import unique_otp_generator
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


import random 
import os


class UserManager(BaseUserManager):

    def create_user(self, phone, is_staff=False, name=None, password=None, is_agent=False, is_active=True, 
                    is_admin=False, is_shop_assistant=False, is_client=False):

        if not phone:
            raise ValueError('users must have a phone number')
        if not password:
            raise ValueError('user must have a password')

        user_obj = self.model(
            phone=phone
        )
        user_obj.set_password(password)
        user_obj.is_staff = is_staff
        user_obj.name = name
        user_obj.agent = is_agent
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.shop_assistant =is_shop_assistant
        user_obj.client = is_client
        user_obj.save(using=self._db)

        return user_obj


    def create_agentuser(self, phone, password=None):

        user = self.create_user(
            phone,
            password=password,
            is_agent=True,
        )

        return user



    def create_shopassistantuser(self, phone, password=None):

        user = self.create_user(
            phone,
            password=password,
            is_shop_assistant=True,
        )

        return user



    def create_clientuser(self, phone, password=None):

        user = self.create_user(
            phone,
            password=password,
            is_client=True,
        )

        return user



    def create_superuser(self, phone, password=None):

        user = self.create_user(
            phone,
            password=password,
            is_admin=True,
            is_staff=True
        )

        return user



class Client(AbstractBaseUser):
    
    phone_regex =   RegexValidator(regex=r'^(\+\d{1,3})?,?\s?\d{10,14}', message = "Phone number must be entered in the format: '+9999999999'. Up to 14 digits are allowed")
    phone =         models.CharField(validators=[phone_regex], max_length=15, unique=True)
    name =          models.CharField(max_length=200, blank=True, null=True)

    usd_balance = models.FloatField(default=0)
    cdf_balance = models.FloatField(default=0)


    is_staff = models.BooleanField(default=False)

    active =        models.BooleanField(default=False)
    shop_assistant =         models.BooleanField(default=False)
    client =         models.BooleanField(default=False)
    agent =         models.BooleanField(default=False)
    admin =         models.BooleanField(default=False)
    date_joined =     models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()


    def __str__(self):
        return self.phone

    def get_full_name(self):
        if self.name :
            return self.name
        else :
            return self.phone

    def get_short_name(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_agent(self):
        return self.agent


    @property
    def is_client(self):
        return self.client
    

    @property
    def is_shop_assistant(self):
        return self.shop_assistant


    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active
    


class PhoneOTP(models.Model):
    phone_regex = RegexValidator(regex=r'^(\+\d{1,3})?,?\s?\d{9,14}', message ="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.")
    phone       = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    otp         = models.CharField(max_length = 9, blank = True, null= True)
    validated   = models.BooleanField(default= False, help_text='If it true, that means user have validate otp correctly in second API')

    def __str__(self):
        return str(self.phone) + ' is sent ' + str(self.otp)
