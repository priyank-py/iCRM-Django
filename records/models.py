from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from employees.models import Employee
from django.utils import timezone


# class MyMonthlyTarget(models.Model):
#     positions_available = (
#         ('telecaller', 'Telecaller'),
#         ('frontdesk', 'Front Desk'),
#         ('counselor', 'Counselor'),
#         ('bde', 'BDE'),
#         ('admin', 'Admin'),
#         ('developer', 'Developer'),
#         ('manager', 'Manager'),
#         ('seniormanager', 'Senior Manager'),
#     )
#     user = models.ForeignKey(User , on_delete=models.CASCADE, blank=True, null=True)
#     position = models.CharField(choices=positions_available, max_length=100)
#     month = models.CharField(default=datetime.now().strftime('%B'), max_length=50)
#     mails = models.IntegerField(default=0)
#     messages = models.IntegerField(default=0)
#     calls = models.IntegerField(default=0)
#     online_submissions = models.IntegerField(default=0)
#     follow_ups = models.IntegerField(default=0)

#     def __str__(self):
#         return f'{self.position} <{self.month}>'   

    # def get_absolute_url(self):
    #     return reverse("EmpRecord_detail", kwargs={"pk": self.pk})


class EmpRecord(models.Model):
    
    employee = models.ForeignKey(User, related_name='user_profile', on_delete=models.DO_NOTHING, blank=True, null=True)
    mails = models.IntegerField(blank=True, null=True, default=0)
    messages = models.IntegerField(blank=True, null=True, default=0)
    calls = models.IntegerField(blank=True, null=True, default=0)
    online_submissions = models.IntegerField(blank=True, null=True, default=0)
    follow_ups = models.IntegerField(blank=True, null=True, default=0)
    submitted_on = models.DateTimeField(blank=True, null=True, default=datetime.now)
    

    # class Meta:
    #     verbose_name = _("EmpRecord")
    #     verbose_name_plural = _("EmpRecords")

    def __str__(self):
        return self.employee.username

class EmpCustomRecord(models.Model):
    emp_record = models.ForeignKey(EmpRecord, related_name="custom_record", on_delete=models.DO_NOTHING)
    field_name = models.CharField(max_length=60, blank=True, null=True, verbose_name="Custom Records")
    value = models.IntegerField(blank=True, null=True, default=0)

class MonthlyTarget(EmpRecord):
    positions_available = (
        ('telecaller', 'Telecaller'),
        ('frontdesk', 'Front Desk'),
        ('counselor', 'Counselor'),
        ('bde', 'BDE'),
        ('admin', 'Admin'),
        ('developer', 'Developer'),
        ('manager', 'Manager'),
        ('seniormanager', 'Senior Manager'),
    )
    position = models.CharField(choices=positions_available, max_length=100)
    month = models.CharField(default=datetime.now().strftime('%B'), max_length=50)

    # submitted_on = models.DateTimeField(blank=True, null=True, default=datetime.now, verbose_name="Created On")
    # mails = models.IntegerField(default=0)
    # messages = models.IntegerField(default=0)
    # calls = models.IntegerField(default=0)
    # online_submissions = models.IntegerField(default=0)
    # follow_ups = models.IntegerField(default=0)
    # employee =  models.ForeignKey(EmpRecord, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.position} <{self.month}>'



class DTS(models.Model):

    employee = models.ForeignKey(Employee, related_name='reporter', on_delete=models.DO_NOTHING, blank=True, null=True)
    dated = models.DateTimeField(unique=True, default=timezone.now, blank=True)

    def __str__(self):
        return self.employee.name

class TargetData(models.Model):
    emp = models.ForeignKey(DTS, related_name='start_data', on_delete=models.CASCADE, blank=True, null=True)
    start = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    end = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    task = models.CharField(max_length=200,blank=True, null=True)
    remark = models.CharField(max_length=50, blank=True, null=True)

    # def __str__(self):
    #     return self.emp.employee

class AchievedData(models.Model):
    emp = models.ForeignKey(DTS, related_name='final_data', on_delete=models.CASCADE, blank=True, null=True)
    start = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    end = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    task = models.CharField(max_length=200,blank=True, null=True)
    remark = models.CharField(max_length=50, blank=True, null=True)
    

