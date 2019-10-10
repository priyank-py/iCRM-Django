from django.db import models
from leads.models import Lead, CorporateAndInstitutionLead
from employees.models import Employee
from django.utils import timezone
from django.utils.translation import gettext as _
from math import ceil

# Create your models here.


class Invoice(models.Model):
    CHOICES = (('Java','Java'),('Python','Python'),('Php','Php'))
    lead = models.ForeignKey(Lead, verbose_name=_("Lead"), related_name='lead_invoice', on_delete=models.CASCADE)
    # dated = models.DateField(blank=True, null=True)
    enquired_for = models.CharField(_("Service Taken"), max_length=50, blank=True, null=True)
    batchstartdate = models.DateField(_("Batch Start Date"), blank=True, null=True, default=None)
    counselor = models.ForeignKey(Employee, verbose_name=_("Counseled by"), on_delete=models.CASCADE)
    
    bal_amount = models.IntegerField(_("Due Amount"), blank=True, null=True)
    due_date = models.DateField(_("Dues pay date"), blank=True, null=True)
    add_fee = models.IntegerField(_("Admission Fee"), blank=True,null=True)
    course_ware_fee = models.IntegerField(blank=True,null=True)
    tution_fee = models.IntegerField(blank=True,null=True)
    project_fee = models.IntegerField(blank=True,null=True)
    late_fee = models.IntegerField(blank=True,null=True)
    exam_fee = models.IntegerField(blank=True,null=True)
    other = models.IntegerField(blank=True,null=True)
    # coorporate_gst = models.CharField(max_length=50,blank=True,null=True)
    sub_total = models.IntegerField(blank=True,null=True)
    gst = models.CharField(max_length=50,blank=True,null=True)
    g_total = models.IntegerField(_("Grand Total"), blank=True,null=True)
    amount_words = models.CharField(_("Amount in word"), max_length=200, blank=True, null=True)

    def save(self, *args, **kwargs):
        def num2words(num):
            under_20 = ['Zero','One','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Eleven','Twelve','Thirteen','Fourteen','Fifteen','Sixteen','Seventeen','Eighteen','Nineteen']
            tens = ['Twenty','Thirty','Forty','Fifty','Sixty','Seventy','Eighty','Ninety']
            above_100 = {100: 'Hundred',1000:'Thousand', 1000000:'Million', 1000000000:'Billion'}
        
            if num < 20:
                return under_20[num]
            
            if num < 100:
                return tens[(int)(num/10)-2] + ('' if num%10==0 else ' ' + under_20[num%10])
        
            # find the appropriate pivot - 'Million' in 3,603,550, or 'Thousand' in 603,550
            pivot = max([key for key in above_100.keys() if key <= num])
        
            return num2words((int)(num/pivot)) + ' ' + above_100[pivot] + ('' if num%pivot==0 else ' ' + num2words(num%pivot))
        values = [self.add_fee, self.course_ware_fee, self.tution_fee, self.project_fee, self.exam_fee, self.late_fee, self.other]
        self.sub_total = ceil(sum([i for i in values if i != None]))
        self.gst = self.sub_total * 0.18
        self.g_total = ceil(self.sub_total + self.gst)
        self.amount_words = num2words(self.g_total)
        super(Invoice, self).save(*args, **kwargs)

    @property
    def lead_name(self):
        return self.lead.lead_name

    def __str__(self):
        return f'{self.lead}'


class InstallmentData(models.Model):
    payment_status = ((True, 'Paid'), (False, 'Unpaid'))
    invoice = models.ForeignKey(Invoice, verbose_name=_(""), on_delete=models.CASCADE)
    installment_date = models.DateField(_("Date"), auto_now=False, auto_now_add=False, blank=True, null=True)
    installment_amount = models.IntegerField(_("Amount"), blank=True, null=True)
    paid = models.BooleanField(_("Payment Status"), choices=payment_status, default=False, blank=True, null=True)


class Bill(models.Model):
    
    pay_options = (('cash', 'Cash'), ('cheque', 'Cheque'), ('card', 'Card'), ('online', 'Online'))

    invoice = models.ForeignKey(Invoice, related_name='source_invoice', on_delete=models.CASCADE)
    bill_number = models.PositiveSmallIntegerField(_("Bill#"), blank=True, null=True)
    bill_date = models.DateField(blank=True, null=True, default=timezone.now)
    # client = models.CharField(max_length=30,blank=True,null=True)
    payment_option = models.CharField(_("Pay Option"), max_length=30, choices=pay_options)
    recieve_amount = models.IntegerField(_("Recieved Amount"), blank=True, null=True)
    amount_in_word = models.CharField(_("Amount in Words"), max_length=50, blank=True, null=True)    

    #crdname=models.CharField(max_length=200)
    credit_card_no = models.CharField(_("Credit/Debit Card No."), blank=True, null=True, default=None, max_length=20)
    dd_no = models.CharField(_("DD No."), blank=True, null=True, max_length=20, default=None)
    cheque_no = models.CharField(blank=True, null=True, max_length=20, default=None)
    drawn_on = models.CharField(blank=True, null=True, max_length=20, default=None)

    class Meta:
        verbose_name = _("Bill")
        verbose_name_plural = _("Bills")

    
    def save(self, *args, **kwargs):
        def num2words(num):
            under_20 = ['Zero','One','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Eleven','Twelve','Thirteen','Fourteen','Fifteen','Sixteen','Seventeen','Eighteen','Nineteen']
            tens = ['Twenty','Thirty','Forty','Fifty','Sixty','Seventy','Eighty','Ninety']
            above_100 = {100: 'Hundred',1000:'Thousand', 1000000:'Million', 1000000000:'Billion'}
        
            if num < 20:
                return under_20[num]
            
            if num < 100:
                return tens[(int)(num/10)-2] + ('' if num%10==0 else ' ' + under_20[num%10])
        
            # find the appropriate pivot - 'Million' in 3,603,550, or 'Thousand' in 603,550
            pivot = max([key for key in above_100.keys() if key <= num])
        
            return num2words((int)(num/pivot)) + ' ' + above_100[pivot] + ('' if num%pivot==0 else ' ' + num2words(num%pivot))
        self.amount_in_word = num2words(ceil(self.recieve_amount))
        super(Bill, self).save(*args, **kwargs)


    def __str__(self):
        return f'{self.invoice.id}'

    # def get_absolute_url(self):
    #     return reverse("Bill_detail", kwargs={"pk": self.pk})



class ClientInvoice(models.Model):

    lead = models.ForeignKey(CorporateAndInstitutionLead, verbose_name=_("Client"), on_delete=models.CASCADE)
    enquired_for = models.CharField(_("Service Taken"), max_length=50, blank=True, null=True)
    batchstartdate = models.DateField(_("Batch Start Date"), blank=True, null=True, default=None)
    counselor = models.ForeignKey(Employee, verbose_name=_("Counseled by"), on_delete=models.CASCADE)
    
    bal_amount = models.IntegerField(_("Due Amount"), blank=True, null=True)
    due_date = models.DateField(_("Dues pay date"), blank=True, null=True)
    add_fee = models.IntegerField(_("Admission Fee"), blank=True,null=True)
    course_ware_fee = models.IntegerField(blank=True,null=True)
    tution_fee = models.IntegerField(blank=True,null=True)
    project_fee = models.IntegerField(blank=True,null=True)
    late_fee = models.IntegerField(blank=True,null=True)
    exam_fee = models.IntegerField(blank=True,null=True)
    other = models.IntegerField(blank=True,null=True)
    # coorporate_gst = models.CharField(max_length=50,blank=True,null=True)
    sub_total = models.IntegerField(blank=True,null=True)
    gst = models.CharField(max_length=50,blank=True,null=True)
    g_total = models.IntegerField(_("Grand Total"), blank=True,null=True)
    amount_words = models.CharField(_("Amount in word"), max_length=200, blank=True, null=True)

    def save(self, *args, **kwargs):
        def num2words(num):
            under_20 = ['Zero','One','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Eleven','Twelve','Thirteen','Fourteen','Fifteen','Sixteen','Seventeen','Eighteen','Nineteen']
            tens = ['Twenty','Thirty','Forty','Fifty','Sixty','Seventy','Eighty','Ninety']
            above_100 = {100: 'Hundred',1000:'Thousand', 1000000:'Million', 1000000000:'Billion'}
        
            if num < 20:
                return under_20[num]
            
            if num < 100:
                return tens[(int)(num/10)-2] + ('' if num%10==0 else ' ' + under_20[num%10])
        
            # find the appropriate pivot - 'Million' in 3,603,550, or 'Thousand' in 603,550
            pivot = max([key for key in above_100.keys() if key <= num])
        
            return num2words((int)(num/pivot)) + ' ' + above_100[pivot] + ('' if num%pivot==0 else ' ' + num2words(num%pivot))
        values = [self.add_fee, self.course_ware_fee, self.tution_fee, self.project_fee, self.exam_fee, self.late_fee, self.other]
        self.sub_total = ceil(sum([i for i in values if i != None]))
        self.gst = self.sub_total * 0.18
        self.g_total = ceil(self.sub_total + self.gst)
        self.amount_words = num2words(self.g_total)
        super(ClientInvoice, self).save(*args, **kwargs)

    @property
    def lead_name(self):
        return self.lead.name

    def __str__(self):
        return f'{self.lead}'
    

    class Meta:
        verbose_name = _("ClientInvoice")
        verbose_name_plural = _("ClientInvoices")

    def __str__(self):
        return self.name

class ClientInstallmentData(models.Model):

    invoice = models.ForeignKey(ClientInvoice, verbose_name=_(""), on_delete=models.CASCADE)
    payment_status = ((True, 'Paid'), (False, 'Unpaid'))
    installment_date = models.DateField(_("Date"), auto_now=False, auto_now_add=False, blank=True, null=True)
    installment_amount = models.IntegerField(_("Amount"), blank=True, null=True)
    paid = models.BooleanField(_("Payment Status"), choices=payment_status, default=False, blank=True, null=True)



class ClientBill(models.Model):
 
    pay_options = (('cash', 'Cash'), ('cheque', 'Cheque'), ('card', 'Card'), ('online', 'Online'))
    
    invoice = models.ForeignKey(ClientInvoice, verbose_name=_(""), on_delete=models.CASCADE)
    bill_number = models.PositiveSmallIntegerField(_("Bill#"), blank=True, null=True)
    bill_date = models.DateField(blank=True, null=True, default=timezone.now)
    # client = models.CharField(max_length=30,blank=True,null=True)
    payment_option = models.CharField(_("Pay Option"), max_length=30, choices=pay_options)
    recieve_amount = models.IntegerField(_("Recieved Amount"), blank=True, null=True)
    amount_in_word = models.CharField(_("Amount in Words"), max_length=50, blank=True, null=True)    

    #crdname=models.CharField(max_length=200)
    credit_card_no = models.CharField(_("Credit/Debit Card No."), blank=True, null=True, default=None, max_length=20)
    dd_no = models.CharField(_("DD No."), blank=True, null=True, max_length=20, default=None)
    cheque_no = models.CharField(blank=True, null=True, max_length=20, default=None)
    drawn_on = models.CharField(blank=True, null=True, max_length=20, default=None)

    class Meta:
        verbose_name = _("Bill")
        verbose_name_plural = _("Bills")

    
    def save(self, *args, **kwargs):
        def num2words(num):
            under_20 = ['Zero','One','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Eleven','Twelve','Thirteen','Fourteen','Fifteen','Sixteen','Seventeen','Eighteen','Nineteen']
            tens = ['Twenty','Thirty','Forty','Fifty','Sixty','Seventy','Eighty','Ninety']
            above_100 = {100: 'Hundred',1000:'Thousand', 1000000:'Million', 1000000000:'Billion'}
        
            if num < 20:
                return under_20[num]
            
            if num < 100:
                return tens[(int)(num/10)-2] + ('' if num%10==0 else ' ' + under_20[num%10])
        
            # find the appropriate pivot - 'Million' in 3,603,550, or 'Thousand' in 603,550
            pivot = max([key for key in above_100.keys() if key <= num])
        
            return num2words((int)(num/pivot)) + ' ' + above_100[pivot] + ('' if num%pivot==0 else ' ' + num2words(num%pivot))
        self.amount_in_word = num2words(ceil(self.recieve_amount))
        super(ClientBill, self).save(*args, **kwargs)


    def __str__(self):
        return f'{self.invoice.id}'
