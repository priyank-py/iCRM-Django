from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('profile', views.profile, name='myprofile'),
    path('reports', views.my_reports, name='reports'),
    path('icons', views.icons, name='icons'),
    path('logout', views.logout_view, name='logout'),
    path('notifications', views.notifications, name='notifications'),
    path('seven', views.sales_last_seven_days, name='seven'),
]
