from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('profile', views.profile, name='myprofile'),
    path('icons', views.icons, name='icons'),
    path('logout', views.logout_view, name='logout')

]
