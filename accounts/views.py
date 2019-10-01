from django.shortcuts import render

# Create your views here.
def reciept(request):
    
    context = {}
    return render(request, 'pages/invoice.html', context)