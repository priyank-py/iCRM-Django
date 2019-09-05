from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

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

    # def get_absolute_url(self):
    #     return reverse("EmpRecord_detail", kwargs={"pk": self.pk})



