from django.shortcuts import render, redirect
from .forms import RegisterForm
from employees.models import Employee

# Create your views here.
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid:
            form.save()
        return redirect('profile')
    else:
        form = RegisterForm()
    return render(response, 'pages/register.html', {'form':form})


def profile(request):
    emps = Employee.objects.all()

    current_user = request.user

    context = {
        'emps': emps,
        'current_user': current_user
    }
    return render(request, 'pages/profile.html', context)
