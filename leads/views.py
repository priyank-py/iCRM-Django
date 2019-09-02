from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import Lead
# from .forms import LeadForm, RemarksModelFormset

# Create your views here.
def new_leads(request):
    leads = Lead.objects.order_by('-generation_at').filter(is_counseled=False)

    paginator = Paginator(leads, 3)
    page = request.GET.get('page')
    paged_leads = paginator.get_page(page)

    context = {
        'leads': paged_leads
    }
    return render(request, 'leads/listings.html', context)

def all_leads(request):
    leads = Lead.objects.all()

    paginator = Paginator(leads, 3)
    page = request.GET.get('page')
    paged_leads = paginator.get_page(page)

    context = {
        'leads': paged_leads
    }
    return render(request, 'leads/all_leads.html', context)

# def listing(request):
#     return render(request, 'leads/listing.html')


def search(request):
    return render(request, 'leads/search.html')


# def generate(response):
#     if response.method == "POST":
#         form = RemarksModelFormset(response.POST)
#         if form.is_valid:
#             form.save()
#         return redirect('generate')
#     else:
#         form = RemarksModelFormset()
#     return render(response, 'pages/generation.html', {'form':form})

