from django.shortcuts import render, redirect
from employees.models import Employee
from leads.models import Lead
import datetime
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

@login_required(login_url='admin:login')
def dashboard(request):
    # emps = Employee.objects.all()
    emp = request.user
    emps = emp.profile.get_descendants(include_self=False)
    leads = Lead.objects.all()
    total_col = 0
    for i in leads:
        if i.course_fee:
            total_col += i.course_fee

    follow_leads = Lead.objects.all().filter(is_counseled=True).filter(next_follow_up_date__lte=datetime.date.today())

    # total_new = len(new_leads)

    context = {
        'emps': emps,
        'leads': leads,
        'total_col': total_col,
        'follow_leads': follow_leads,
    }
    return render(request, 'pages/my_panel.html', context)


# def notification(request):
#     follow_leads = Lead.objects.all().filter(is_counseled=True).filter(next_follow_up_date__lte=datetime.date.today())
    
#     context = {'follow_leads': follow_leads,}

#     return render(request, 'partials/_dash_navbar.html', context)


@login_required
def profile(request):
    emps = Employee.objects.all()

    current_user = request.user
    emp = Employee.objects.filter(name=current_user)
  
    context = {
        'emps': emps,
        'current_user': current_user,
        'emp': emp,
    }
    return render(request, 'pages/myprofile.html', context)


@login_required
def my_reports(request):
    return render(request, 'pages/my_reports.html')


@login_required
def notifications(request):
    info = Lead.objects.all().order_by('-generation_at').filter(assigned_to_id=request.user.id).filter(is_counseled=False)
    success = Lead.objects.filter(is_counseled=True).filter(status='Walk in registered')
    current_user = request.user.id
    context = {
        'info': info,
        'success': success,
        'current_user': current_user,
    }
    return render(request, 'pages/notifications.html', context)


@login_required
def icons(request):
    return render(request, 'pages/icons.html')


@login_required
def logout_view(request):
    logout(request)
    return render(request, 'pages/index.html')





def sales_last_seven_days(request):
    delta = 0
    todays_day = datetime.date.today().weekday()
    registered_leads = [i if not i==None or i==0 else 0 for i in Lead.objects.values_list('course_fee', flat=True).filter(status='Walk in registered')]   
    context = {

        'colls': registered_leads
    }
    return render(request, 'pages/collection_data.html', context)


