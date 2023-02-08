from django.contrib import admin

from .models import *


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'password', 'designation', 'inventory', 'personal_email',
                    'gender', 'temperory_address', 'permanent_address', 'phone_number', 'alternate_phone_number',
                    'department', 'joined_date', 'image', 'created_at', 'updated_at')


class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'role_name', 'created_at', 'updated_at')


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'department_name', 'created_at', 'updated_at')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Department, DepartmentAdmin)
