from django import forms
from .models import EmpRecord


class EmpRecordForm(forms.ModelForm):
    
    class Meta:
        model = EmpRecord
        fields = '__all__'

