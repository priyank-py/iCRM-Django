from django.shortcuts import render, get_object_or_404
from .models import Invoice, Bill

# Create your views here.
def invoices(request):
    get_invoices = Invoice.objects.all()
    context = {'get_invoices': get_invoices,}
    return render(request, 'pages/invoices.html', context)


def reciept(request, id):
    invoice = get_object_or_404(Invoice, pk=id)
    bills = Bill.objects.order_by('-id').filter(invoice=invoice)

    context = {
        'invoice': invoice,
        'bills': bills,
    }

    return render(request, 'commerce/invoice.html', context)



def quotation(request):

    context = {}

    return render(request, 'pages/quotation.html', context)