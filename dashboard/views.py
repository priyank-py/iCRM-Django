from django.shortcuts import render, redirect
from employees.models import Employee
from leads.models import Lead, LeadRemarks
from records.models import MonthlyTarget, EmpRecord
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

    latest_lead_remark = [i.lead_remarks.last() for i in leads]
    registered_lead_ids = [i.lead.id for i in latest_lead_remark if i.status == 'walkinreg']
    registered_lead_ids_past_seven_days = [i.lead for i in latest_lead_remark if i.status == 'walkinreg' and i.next_follow_up_date > date.today() - timedelta(days=7)]
    past_seven_days = [calendar.day_name[(date.today() - timedelta(days=i)).weekday()] for i in range(6, -1, -1)]
    registered_each_days = [sum([i.course_fee for i in registered_lead_ids_past_seven_days if i.lead_remarks.last().next_follow_up_date == date.today() - timedelta(days=j)]) for j in range(6, -1, -1)]
    total_col = 0
    last_week = datetime.now() - timedelta(days=7)

    # weekly_data = Lead.objects.filter(id__in=registered_lead_ids).extra(select={'day': 'date(lead_remarks.last().next_follow_up_date)'}).values('day').annotate(sum=Sum('course_fee'))
    
    weekly_data = Lead.objects.filter(id__in=registered_lead_ids).filter()

    # seven_days = []
    # seven_data = []
    min_data = 0
    max_data = 1000
    # for dates in weekly_data:
    #     dates['day'] = datetime.strptime(dates['day'], '%Y-%m-%d')
    #     days = datetime.strftime(dates['day'], '%a')
    #     dates['day'] = days
    # seven_days = [i['day'] for i in weekly_data]
    # seven_data = [j['sum'] for j in weekly_data]
    
    current_month = int(datetime.now().strftime('%m'))
    current_year = int(datetime.now().strftime('%Y'))
    first_day, last_day = calendar.monthrange(current_year, current_month)
    start_month_date = datetime.today().replace(day=1)
    end_month_date = datetime.today().replace(day=last_day)

    seven_days = [i[:3] for i in past_seven_days]
    seven_data = registered_each_days

    try:
        month_targets = MonthlyTarget.objects.all().filter(month=datetime.now().strftime('%B')).filter(position=emp.profile.postion)
    except:
        month_targets = MonthlyTarget.objects.none()
        print('Targets Not Added Yet!')
    
    emp_monthly_records = EmpRecord.objects.all().filter(submitted_on__gte=start_month_date).filter(submitted_on__lte=end_month_date)



    if any(seven_data):
        min_data = min(seven_data) - 1000
        max_data = max(seven_data) + 1000

    last_month = datetime.now() - timedelta(days=30)
    tech_data = Lead.objects.filter(id__in=registered_lead_ids).extra(select={'tech': 'enquired_for'}).values('tech').annotate(sum=Sum('course_fee'))
    
  
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

    # follow_leads = LeadRemarks.objects.all().filter(next_follow_up_date__lte=date.today()).latest('next_follow_up_date')
    # unregistered_leads = [l.lead.id for l in follow_leads if l.status !='walkinreg' or l.status !='leadreg']
    # print(unregistered_leads)
    # follow_leads = Lead.objects.filter(id__in=unregistered_leads)

    # all_lead = Lead.objects.all()
    # latest_lead_remark = [i.lead_remarks.last() for i in all_lead]
    for data in latest_lead_remark:
        print('This the what i looking for: ',data.next_follow_up_date)
    # unregistered_leads = [l.lead.id for l in follow_lead if l.status !='walkinreg' or l.status !='leadreg']
    # print(unregistered_leads)
    # follow_leads = Lead.objects.filter(id__in=unregistered_leads)

    # total_new = len(new_leads)
    morning_report = DTS.objects.all().filter(dated=date.today()).filter(employee=request.user.profile)

    leadclose = [i.lead for i in latest_lead_remark if i.status == 'leadclose']
    leadwalkin = [i.lead for i in latest_lead_remark if i.status == 'leadwalkin']
    leadfollowup = [i.lead for i in latest_lead_remark if i.status == 'leadfollowup']
    leadreg = [i.lead for i in latest_lead_remark if i.status == 'leadreg']
    walkinfollowup = [i.lead for i in latest_lead_remark if i.status == 'walkinfollowup']
    walkinreg = [i.lead for i in latest_lead_remark if i.status == 'walkinreg']
    walkindeclaration = [i.lead for i in latest_lead_remark if i.status == 'walkindeclaration']
    walkinclose = [i.lead for i in latest_lead_remark if i.status == 'walkinclose']

    category_data = [leadclose,
    leadwalkin,
    leadfollowup,
    leadreg,
    walkinfollowup,
    walkinreg,
    walkindeclaration,
    walkinclose]

    category_names = ['leadclose', 'leadwalkin', 'leadfollowup', 'leadreg', 'walkinfollowup', 'walkinreg', 'walkindeclaration', 'walkinclose']

    category_count = [len(i) if any(i) else 0 for i in category_data]

    print('Number of student in by category',category_count)


    context = {
        'emps': emps,
        'leads': leads,
        'total_col': total_col,
        # 'follow_leads': follow_leads,
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
        'category_names': category_names,
        'category_count': category_count,
        'month_targets': month_targets,
        'emp_monthly_records': emp_monthly_records,
    }
    # if any(follow_leads):
    #     context['follow_leads'] = follow_leads

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


