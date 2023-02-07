from django.contrib import admin

from .models import *
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'password','role', 'personal_email','gender', 'temperory_address','permanent_address','phone_number','alternate_phone_number','department', 'joined_date', 'image')

# Register your models here.
class RoleAdmin(admin.ModelAdmin):
    list_display = ('role_name',)

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('department_name',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Department, DepartmentAdmin)