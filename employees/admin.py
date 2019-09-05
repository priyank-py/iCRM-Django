from django.contrib import admin
from .models import Employee
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django import forms

# Register your models here.

class UserEmployeeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserEmployeeForm, self).__init__(*args, **kwargs)
        if self.instance.pk is None:
            self.empty_permitted = False # Here

    class Meta:
        model = Employee
        fields = '__all__'



class EmployeeInline(admin.StackedInline):
    model = Employee
    form = UserEmployeeForm
    can_delete = False
    fk_name='user'
    extra = 1
    max_num = 1
    min_num = 1

# class EmployeeAdmin(admin.ModelAdmin):
#     list_display = ('name', 'postion', 'email', 'hire_date')
#     list_display_links = ('name', 'email')
    


class EmployeeUserAdmin(UserAdmin):


    inlines = (EmployeeInline,)
    list_select_related = ('profile', )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(EmployeeUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, EmployeeUserAdmin)
