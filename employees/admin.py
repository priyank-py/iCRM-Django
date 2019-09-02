from django.contrib import admin
from .models import Employee

# Register your models here.

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'postion', 'email', 'hire_date')
    list_display_links = ('name', 'email')


admin.site.register(Employee, EmployeeAdmin)
