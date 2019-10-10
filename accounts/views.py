from django.shortcuts import render, get_object_or_404
from .models import Invoice, Bill, InstallmentData
from leads.models import CorporateAndInstitutionLead, Quotation
from django.core.mail import send_mail
from django.http import HttpResponse

# Create your views here.
def invoices(request):
    get_invoices = Invoice.objects.all()
    get_both = [(Bill.objects.all().filter(invoice=i), i) for i in get_invoices]
    
    context = {'get_both': get_both,}
    return render(request, 'pages/invoices.html', context)


def lead_invoice(request, id):
    invoice = get_object_or_404(Invoice, pk=id)
    installments = InstallmentData.objects.order_by('-id').filter(invoice=invoice)
    bills = Bill.objects.order_by('-id').filter(invoice=invoice)

    context = {
        'invoice': invoice,
        'bills': bills,
        'installments': installments,
    }

    return render(request, 'commerce/invoice.html', context)


def each_bill(request, id):
    bill = get_object_or_404(Bill, pk=id)
    context = {'bill': bill}
    return render(request, 'commerce/bill.html', context)


def all_quotation(request):
    quotes = Quotation.objects.all()
    context = {
        'quotes': quotes,
    }
    return render(request, 'pages/quotes.html')


def quotation(request, id):
    quote = get_object_or_404(Quotation, pk=id)

    context = {'quote': quote}

    return render(request, 'commerce/quote.html', context)


# def sendRecieptEmail(request,emailto):
#    res = send_mail("hello paul", "comment tu vas?", "factscred@gmail.com", [emailto])
#    return HttpResponse('%s'%res)