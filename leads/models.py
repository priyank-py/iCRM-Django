from django.db import models
import datetime
from employees.models import Employee
from django.utils import timezone
from taggit.managers import TaggableManager

# Create your models here.
available_status = (('leadclose', 'Lead Closed'), ('leadwalkin', 'Lead walked in'), ('leadfollowup', 'Leads follow up'), ('walkinfollowup', 'Walk in follow up'), ('walkinreg', 'Walk in registered'), ('walkinclose', 'Walk in closed'))
YEAR_CHOICES = [(i, i) for i in range(1980, (int(datetime.datetime.now().year)+4))]


class Lead(models.Model):
    lead_id = models.PositiveIntegerField(null=True, blank=True)
    lead_name = models.CharField(max_length=150)
    lead_email = models.EmailField(null=True, blank=True)
    lead_phone = models.CharField(max_length=20)
    campaign_remarks = models.CharField(max_length=255, null=True, blank=True)
    enquired_for = models.CharField(max_length=250, null=True, blank=True)
    skills_known = TaggableManager()
    counselor_name = models.CharField(max_length=100, null=True, blank=True)
    course_fee = models.IntegerField(null=True, blank=True, default=0)
    status = models.CharField(max_length=200, choices=available_status, default='', null=True, blank=True)
    # assigned_to = models.CharField(max_length=200, choices=available_status, default='')
    highest_qualification = models.CharField(max_length=200, null=True, blank=True)
    Year_of_passing = models.IntegerField(null=True, blank=True, choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    location = models.CharField(max_length=200, null=True, blank=True)
    # remarks = models.TextField(null=True, blank=True)
    next_follow_up_date = models.DateField(null=True, blank=True)
    final_report = models.CharField(max_length=150, null=True, blank=True)
    lead_image = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    is_counseled = models.BooleanField(default=False)
    # user = models.ForeignKey(User,related_name='lead',related_query_name='lead',on_delete=models.CASCADE)
    generation_at = models.DateTimeField(blank=True, null=True)    
    assigned_to = models.ForeignKey(Employee, related_name='counselor', on_delete=models.DO_NOTHING, blank=True, null=True)
    registration_date = models.DateTimeField(blank=True, null=True)
    

    def __str__(self):
        return self.lead_name


class LeadRemarks(models.Model):

    lead = models.ForeignKey(Lead, related_name='lead_remarks', on_delete=models.CASCADE)
    remarks = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.lead.lead_name
