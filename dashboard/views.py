from django.shortcuts import render, redirect
from employees.models import Employee
from leads.models import Lead, LeadRemarks
# import datetime
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models import Sum
from datetime import datetime, timedelta, date
import calendar
from records.models import DTS

@login_required(login_url='admin:login')
def dashboard(request):
    # emps = Employee.objects.all()
    emp = request.user
    emps = emp.profile.get_descendants(include_self=False)
    leads = Lead.objects.all()
    # seven = Lead.objects.order_by('-registration_date').filter(~Q(registration_date=None))[:7]
    total_col = 0
    last_week = datetime.now() - timedelta(days=7)
    weekly_data = Lead.objects.filter(registration_date__gt=last_week).extra(select={'day': 'date(registration_date)'}).values('day').annotate(sum=Sum('course_fee'))
    
    # seven_days = []
    # seven_data = []
    min_data = 0
    max_data = 1000
    for dates in weekly_data:
        dates['day'] = datetime.strptime(dates['day'], '%Y-%m-%d')
        days = datetime.strftime(dates['day'], '%a')
        dates['day'] = days
    seven_days = [i['day'] for i in weekly_data]
    seven_data = [j['sum'] for j in weekly_data]
    
    if any(seven_data):
        min_data = min(seven_data) - 1000
        max_data = max(seven_data) + 1000

    last_month = datetime.now() - timedelta(days=30)
    tech_data = Lead.objects.filter(registration_date__gt=last_month).extra(select={'tech': 'enquired_for'}).values('tech').annotate(sum=Sum('course_fee'))
    
  
    min_col = 0
    max_col = 1000
    month_course = [i['tech'] for i in tech_data]
    month_course = [''.join([i[0] for i in j.split()]) if len(j.split())>1 else j for j in month_course]
    month_collection = [j['sum'] for j in tech_data]
    if any(month_collection):
        min_col = min(month_collection) - 1000
        max_col = max(month_collection) + 1000
    print(weekly_data)
    for i in leads:
        if i.course_fee:
            total_col += i.course_fee

    follow_leads = LeadRemarks.objects.all().filter(next_follow_up_date__lte=date.today())
    unregistered_leads = [l.id for l in follow_leads if l.lead.status!='walkinreg' or l.lead.status!='leadreg']
    print(unregistered_leads)
    follow_leads = follow_leads.filter(id__in=unregistered_leads)

    # total_new = len(new_leads)
    morning_report = DTS.objects.all().filter(dated=date.today()).filter(employee=request.user.profile)

    context = {
        'emps': emps,
        'leads': leads,
        'total_col': total_col,
        'follow_leads': follow_leads,
        # 'leads_seven': leads_seven,
        'seven_days': seven_days,
        'seven_data': seven_data,
        'min_data': min_data,
        'max_data': max_data,
        'month_course': month_course,
        'month_collection': month_collection,
        'min_col': min_col,
        'max_col': max_col,
        'morning_report': morning_report,
    }
    return render(request, 'pages/my_panel.html', context)


# def notification(request):
#     follow_leads = Lead.objects.all().filter(is_counseled=True).filter(next_follow_up_date__lte=datetime.date.today())
    
#     context = {'follow_leads': follow_leads,}

#     return render(request, 'partials/_dash_navbar.html', context)


@login_required(login_url='admin:login')
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


@login_required(login_url='admin:login')
def my_reports(request):
    emp = request.user
    emps = emp.profile.get_descendants(include_self=True)
    registered_leads = Lead.objects.order_by('-generation_at').filter(~Q(registration_date=None)).filter(assigned_to__in=emps)
    context = {
        'registered_leads': registered_leads,
    }
    return render(request, 'pages/my_reports.html', context)


@login_required(login_url='admin:login')
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


@login_required(login_url='admin:login')
def icons(request):
    return render(request, 'pages/icons.html')


@login_required(login_url='admin:login')
def logout_view(request):
    logout(request)
    return render(request, 'pages/index.html')

def dts(request):
    if request.method == 'POST':
        report = TargetDTS()
        report.task = ''
        for i in range(1, 9):
            if request.POST.get('target{i}') :
                report.task += request.POST.get('target{i}')
               
                report.save()               
                return render(request, 'pages/my_panel.html')  

    else:
            return render(request,'pages/about.html')





def sales_last_seven_days(request):
    delta = 0
    todays_day = date.today().weekday()
    registered_leads = [i if not i==None or i==0 else 0 for i in Lead.objects.values_list('course_fee', flat=True).filter(status='Walk in registered')]   
    context = {

        'colls': registered_leads
    }
    return render(request, 'pages/collection_data.html', context)


