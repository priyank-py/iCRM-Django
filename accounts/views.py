from django.shortcuts import render, get_object_or_404
from .models import Invoice, Bill, InstallmentData, Quotation, QuotationRatesAndTerms
from leads.models import CorporateAndInstitutionLead
from django.core.mail import EmailMessage
from django.http import HttpResponse

#for pdf:
from weasyprint.fonts import FontConfiguration
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from weasyprint import HTML


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
    print(dir(HTML))

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
    rates = QuotationRatesAndTerms.objects.all().filter(quotation=quote)

    context = {
        'quote': quote,
        'rates': rates,
    }

    return render(request, 'commerce/quote.html', context)


# def sendRecieptEmail(request,emailto):
#    res = send_mail("hello paul", "comment tu vas?", "factscred@gmail.com", [emailto])
#    return HttpResponse('%s'%res)

def invoice_to_pdf_view(request, id):

    invoice = get_object_or_404(Invoice, pk=id)
    installments = InstallmentData.objects.order_by('-id').filter(invoice=invoice)
    bills = Bill.objects.order_by('-id').filter(invoice=invoice)
    print(dir(HTML))

    context = {
        'invoice': invoice,
        'bills': bills,
        'installments': installments,
    }

    html_string = render_to_string('commerce/invoice.html', context)
    html = HTML(string=html_string)
    html.write_pdf(target=f'media/invoices/pdf-{id}.pdf')

    # fs = FileSystemStorage('/media/pdfs')
    with open(f'media/invoices/pdf-{id}.pdf', 'rb') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
        font_config = FontConfiguration()
        HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response, font_config=font_config)

        msg = EmailMessage('Subject of the Email', 'Body of the email', 'factscred@gmail.com', ['priyank7137@gmail.com'])
        msg.content_subtype = "html"  
        msg.attach_file(f'media/invoices/pdf-{id}.pdf')
        msg.send()


        return response

    return response

def bill_to_pdf_view(request, id):

    bill = get_object_or_404(Bill, pk=id)
    context = {'bill': bill}

    html_string = render_to_string('commerce/bill.html', context)
    html = HTML(string=html_string)
    html.write_pdf(target=f'media/bills/pdf-{id}.pdf')

    # fs = FileSystemStorage('/media/pdfs')
    with open(f'media/bills/pdf-{id}.pdf', 'rb') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="bill.pdf"'
        font_config = FontConfiguration()
        HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response, font_config=font_config)

        msg = EmailMessage('Subject of the Email', 'Body of the email', 'factscred@gmail.com', ['priyank7137@gmail.com'])
        msg.content_subtype = "html"  
        msg.attach_file(f'media/bills/pdf-{id}.pdf')
        msg.send()


        return response

    return response


def quotation_to_pdf_view(request, id):

    quote = get_object_or_404(Quotation, pk=id)

    context = {'quote': quote}

    html_string = render_to_string('commerce/quotation.html', context)
    html = HTML(string=html_string)
    html.write_pdf(target=f'media/Quotations/pdf-{id}.pdf')

    # fs = FileSystemStorage('/media/pdfs')
    with open(f'media/Quotations/pdf-{id}.pdf', 'rb') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="quotation.pdf"'
        font_config = FontConfiguration()
        HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response, font_config=font_config)

        msg = EmailMessage('Subject of the Email', 'Body of the email', 'factscred@gmail.com', ['priyank7137@gmail.com'])
        msg.content_subtype = "html"  
        msg.attach_file(f'media/Quotations/pdf-{id}.pdf')
        msg.send()


        return response

    return response