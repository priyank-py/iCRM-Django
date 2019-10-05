from django.contrib import admin
from .models import Invoice, Bill
# from admin_numeric_filter.admin import NumericFilterModelAdmin, SingleNumericFilter, RangeNumericFilter, SliderNumericFilter

# Register your models here.


class BillsInline(admin.StackedInline):
    model = Bill
    extra = 1
    fields = ['invoice', 'payment_option', 'credit_card_no', 'dd_no', 'cheque_no', 'drawn_on', 'add_fee', 'course_ware_fee', 'tution_fee', 'project_fee' , 'late_fee', 'exam_fee', 'other', 'amount_words']


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    class Meta:
        model = Invoice
        fields = '__all__'
        # exclude = ('sub_total', 'gst', 'g_total')


class InvoiceAdmin(admin.ModelAdmin):
    class Meta:
        model = Invoice
        fields = '__all__'
    inlines = (BillsInline,)

# admin.site.register(Bill, BillsAdmin)
admin.site.register(Invoice, InvoiceAdmin)