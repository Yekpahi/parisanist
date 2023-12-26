from django.contrib import admin
from userauths.models import Account


class AccountAdmin(admin.ModelAdmin) :
     list_display = ['first_name', 'last_name', 'email']
    
admin.site.register(Account, AccountAdmin)


