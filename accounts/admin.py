from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import CustomUser

# Register your models here.

UserAdmin.fieldsets[2][1]['fields'] = (
    'is_active',
    'is_staff',
    'is_superuser',
    'is_author',
    'special_user_time',
    'groups',
    'user_permissions',   
)
UserAdmin.fieldsets[3][1]["fields"] += ("profile_picture" ,)   

UserAdmin.list_display += ('is_author', 'is_special_user')
        
admin.site.register(CustomUser, UserAdmin)
