from django.contrib import admin
from django.http import HttpResponse
from .models import Lead, LeadRemarks
import csv

class LeadRemarksTabularInline(admin.TabularInline):
    
    model = LeadRemarks
    extra = 1


# Register your models here.
class LeadAdmin(admin.ModelAdmin):
    list_display = ('id', 'lead_name', 'enquired_for', 'is_counseled',)
    list_display_links = ('id', 'lead_name', 'enquired_for')
    list_filter = ('assigned_to', 'year_of_passing_UG')
    list_editable = ('is_counseled',)
    search_fields = ('id', 'lead_name', 'enquired_for', 'technology_based', 'counselor_name', 'year_of_passing_UG')

    # def get_next_follow_up(self, lead):
    #     follow_date = lead.lead_remarks.next_follow_up_date
    #     return follow_date

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

    export_as_csv.short_description = "Export Selected as csv"

    class Meta:
        model = Lead
        fields = '__all__'
    inlines = (LeadRemarksTabularInline, )

 
admin.site.register(Lead, LeadAdmin)
