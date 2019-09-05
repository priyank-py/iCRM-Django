from django.shortcuts import render, redirect
from .forms import EmpRecordForm
from datetime import datetime


def daily_record(request):
    if request.method == "POST":
        form = EmpRecordForm(request.POST)
        if form.is_valid:
            record = form.save(commit=False)
            record.employee = request.user
            form.save()
        return redirect('/')
    else:
        form = EmpRecordForm()
    dt = datetime.now()

    return render(request, 'pages/records.html', {'form':form, 'dt':dt})
