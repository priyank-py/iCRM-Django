from django.urls import path
from . import views

urlpatterns = [
    path('record', views.daily_record, name='record'),
    # path('', views.profile, name='profile')
]