from django.contrib import admin
from django.http import HttpResponse
from .models import EmpRecord
import csv
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter

class EmpRecordAdmin(admin.ModelAdmin):
    list_display = ('employee', 'mails', 'messages', 'calls', 'online_submissions', 'follow_ups', 'submitted_on')
    # list_display_links = ('lead_id', 'lead_name', 'enquired_for')
    list_filter = (('employee'), ('submitted_on', DateTimeRangeFilter))
    # # list_editable = ('is_counseled', 'next_follow_up_date',)
    search_fields = ('employee', 'submitted_on')

    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


admin.site.register(EmpRecord, EmpRecordAdmin)