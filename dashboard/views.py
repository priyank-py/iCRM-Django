from django.shortcuts import render, redirect
from employees.models import Employee
from leads.models import Lead
import datetime
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

@login_required(login_url='admin:login')
def dashboard(request):
    emps = Employee.objects.all()
    leads = Lead.objects.all()
    total_col = 0
    for i in leads:
        if i.course_fee:
            total_col += i.course_fee

    new_leads = Lead.objects.all().filter(is_counseled=False).filter(next_follow_up_date=datetime.date.today())
    # total_new = len(new_leads)

    context = {
        'emps': emps,
        'leads': leads,
        'total_col': total_col,
        'new_leads': new_leads,
    }
    return render(request, 'pages/my_panel.html', context)


@login_required
def profile(request):
    emps = Employee.objects.all()

    current_user = request.user

    context = {
        'emps': emps,
        'current_user': current_user
    }
    return render(request, 'pages/myprofile.html', context)


@login_required
def icons(request):
    return render(request, 'pages/icons.html')


@login_required
def logout_view(request):
    logout(request)
    return render(request, 'pages/index.html')


