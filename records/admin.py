from django.contrib import admin
from .models import EmpRecord

class EmpRecordAdmin(admin.ModelAdmin):
    list_display = ('employee', 'mails', 'messages')
    # list_display_links = ('lead_id', 'lead_name', 'enquired_for')
    # list_filter = ('assigned_to', 'status', 'Year_of_passing')
    # # list_editable = ('is_counseled', 'next_follow_up_date',)
    # search_fields = ('lead_id', 'lead_name', 'enquired_for', 'counselor_name')


admin.site.register(EmpRecord, EmpRecordAdmin)