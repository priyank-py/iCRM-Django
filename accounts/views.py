from django.shortcuts import render, get_object_or_404
from .models import Invoice, Bill, InstallmentData

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


def quotation(request):

    context = {}

    return render(request, 'pages/quotation.html', context)