from django.contrib import admin
from django.http import HttpResponse
from .models import Lead, LeadRemarks
import csv

class LeadRemarksTabularInline(admin.TabularInline):
    model = LeadRemarks
    extra = 1

# Register your models here.
class LeadAdmin(admin.ModelAdmin):
    list_display = ('lead_id', 'lead_name', 'enquired_for')
    list_display_links = ('lead_id', 'lead_name', 'enquired_for')
    list_filter = ('assigned_to', 'status', 'Year_of_passing')
    # list_editable = ('is_counseled', 'next_follow_up_date',)
    search_fields = ('lead_id', 'lead_name', 'enquired_for', 'counselor_name')

    
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

    class Meta:
        model = Lead
        fields = '__all__'
    inlines = (LeadRemarksTabularInline, )

 
admin.site.register(Lead, LeadAdmin)
