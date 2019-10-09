from django.contrib import admin
from .models import Invoice, Bill, InstallmentData
# from admin_numeric_filter.admin import NumericFilterModelAdmin, SingleNumericFilter, RangeNumericFilter, SliderNumericFilter

# Register your models here.

class InstallmentDataInline(admin.StackedInline):
    model = InstallmentData
    extra = 1
    fields = ('installment_date', 'installment_amount', 'paid')


class BillsInline(admin.StackedInline):
    model = Bill
    extra = 1
    fields = ['invoice', 'recieve_amount', 'payment_option', 'credit_card_no', 'dd_no', 'cheque_no', 'drawn_on', 'amount_in_word']


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
    inlines = (InstallmentDataInline, BillsInline,)

# admin.site.register(Bill, BillsAdmin)
admin.site.register(Invoice, InvoiceAdmin)