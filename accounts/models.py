from django.db import models
from leads.models import Lead
from django.utils import timezone
from django.utils.translation import gettext as _

# Create your models here.
class Invoice(models.Model):
    CHOICES = (('Java','Java'),('Python','Python'),('Php','Php'))
    pay_options = (('cash', 'Cash'), ('cheque', 'Cheque'), ('card', 'Card'), ('online', 'Online'))
    lead = models.ForeignKey(Lead, verbose_name=_("Lead"), on_delete=models.CASCADE)

    dated = models.DateField(blank=True,null=True)
    drawn_on = models.DateField(blank=True,null=True)
    recieve_amount=models.IntegerField(blank=True,null=True)
    batchstartdate = models.DateField(blank=True,null=True,default=None)
    counselor = models.CharField(max_length=100,blank=True,null=True)
    
    bal_amount = models.IntegerField(blank=True,null=True)
    due_date = models.DateField(blank=True,null=True)
    # amount_words = models.CharField(max_length=200,blank=True,null=True)
    # client = models.CharField(max_length=30,blank=True,null=True)
    # payment_option = models.BooleanField(_("Pay Option"), choices=pay_options)
    # pay_option1 = models.CharField(max_length=50,blank=True,null=True,default=None)
    # pay_option2 = models.CharField(max_length=50,blank=True,null=True,default=None)
    # pay_option3 = models.CharField(max_length=50,blank=True,null=True,default=None)
    # pay_option4 = models.CharField(max_length=50,blank=True,null=True,default=None)
    # pay_option5 = models.CharField(max_length=50,blank=True,null=True,default=None)
    # add_fee = models.IntegerField(blank=True,null=True)
    # course_ware_fee = models.IntegerField(blank=True,null=True)
    # tution_fee = models.IntegerField(blank=True,null=True)
    # project_fee = models.IntegerField(blank=True,null=True)
    # late_fee = models.IntegerField(blank=True,null=True)
    # exam_fee = models.IntegerField(blank=True,null=True)
    # other = models.IntegerField(blank=True,null=True)
    # coorporate_gst = models.CharField(max_length=50,blank=True,null=True)
    # sub_total = models.IntegerField(blank=True,null=True)
    # gst = models.CharField(max_length=50,blank=True,null=True)
    # g_total = models.IntegerField(blank=True,null=True)

    #crdname=models.CharField(max_length=200)
    # crdno = models.CharField(blank=True,null=True,default=None,max_length=20)
    # ddno = models.CharField(blank=True,null=True,max_length=20,default=None)
    # checkno = models.CharField(blank=True,null=True,max_length=20,default=None)
    # on = models.CharField(blank=True,null=True,max_length=20,default=None)
    # batchstartdate = models.DateField(blank=True,null=True,default=None)
    # counselor = models.CharField(max_length=100,blank=True,null=True)

    @property
    def lead_name(self):
        return self.lead.name

    def __str__(self):
        return self.lead.name

class Bill(models.Model):
    
    pay_options = (('cash', 'Cash'), ('cheque', 'Cheque'), ('card', 'Card'), ('online', 'Online'))

    invoice = models.ForeignKey(Invoice, related_name='source_invoice', on_delete=models.CASCADE)
    client = models.CharField(max_length=30,blank=True,null=True)
    payment_option = models.BooleanField(_("Pay Option"), choices=pay_options)
    ct_fee = models.IntegerField(blank=True,null=True)
    late_fee = models.IntegerField(blank=True,null=True)
    exam_fee = models.IntegerField(blank=True,null=True)
    other = models.IntegerField(blank=True,null=True)
    coorporate_gst = models.CharField(max_length=50,blank=True,null=True)
    sub_total = models.IntegerField(blank=True,null=True)
    gst = models.CharField(max_length=50,blank=True,null=True)
    g_total = models.IntegerField(blank=True,null=True)
    amount_words = models.CharField(max_length=200,blank=True,null=True)

    #crdname=models.CharField(max_length=200)
    crdno = models.CharField(blank=True,null=True,default=None,max_length=20)
    ddno = models.CharField(blank=True,null=True,max_length=20,default=None)
    checkno = models.CharField(blank=True,null=True,max_length=20,default=None)
    on = models.CharField(blank=True,null=True,max_length=20,default=None)

    class Meta:
        verbose_name = _("Bill")
        verbose_name_plural = _("Bills")

    def __str__(self):
        return self.invoice.id

    # def get_absolute_url(self):
    #     return reverse("Bill_detail", kwargs={"pk": self.pk})
