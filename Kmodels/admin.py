from django.contrib import admin

# from __future__ import unicode_literals
from django.contrib.auth import get_user_model
User = get_user_model() 

from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserAdminCreationForm, UserAdminChangeForm

from .models import *
from .clientModel import PhoneOTP, Client
        

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('name', 'phone', 'usd_balance', 'cdf_balance', 'client', 'agent','admin',  
                    'shop_assistant')
    list_filter = ('agent','active' ,'admin', 'client', 'shop_assistant', 'is_staff' )
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': ('name', 'usd_balance', 'cdf_balance', )}),
        ('Permissions', {'fields': ('admin','agent', 'shop_assistant', 'client',
                         'active', 'is_staff')}),
        ('Important dates', {'fields': ('date_joined', 'last_login')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2')}
        ),
    )

    readonly_fields = ['date_joined', 'last_login']


    search_fields = ('phone','name')
    ordering = ('phone','name')
    filter_horizontal = ()



    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)

# admin.site.register(User, UserAdmin)



# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)
    

admin.site.register(Client, UserAdmin)
admin.site.register(PhoneOTP)

admin.site.register(Transaction)
admin.site.register(AgentSupply)
admin.site.register(Bill)