from django.shortcuts import render
from django.http import HttpResponse
import os
import time
from leads.models import Lead
from employees.models import Employee

def index(request):
    leads = Lead.objects.order_by('-generation_at').filter(is_counseled=False)[:3]
    return render(request, 'pages/index.html', {'leads': leads})

def about(request):
    emps = Employee.objects.order_by('-hire_date')[:3]
 
    eom = Employee.objects.filter(is_eom=True)
    
    context = {
        'emps': emps,
        'eom': eom,
    }
    return render(request, 'pages/about.html', context)

