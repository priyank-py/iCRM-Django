from django.contrib import admin
from .models import Invoice, Bill
# from admin_numeric_filter.admin import NumericFilterModelAdmin, SingleNumericFilter, RangeNumericFilter, SliderNumericFilter

# Register your models here.


class BillsAdmin(admin.StackedInline):
    model = Bill
    extra = 1
    fields = ['invoice', 'amount_words', 'client', 'payment_option', 'ct_fee' , 'late_fee', 'exam_fee', 'other', 'coorporate_gst', 'sub_total', 'gst','g_total', 'crdno', 'ddno', 'checkno', 'on']


class InvoiceAdmin(admin.ModelAdmin):
    class Meta:
        model = Invoice
        fields = '__all__'
    inlines = (BillsAdmin,)

# admin.site.register(Bill, BillsAdmin)
admin.site.register(Invoice, InvoiceAdmin)