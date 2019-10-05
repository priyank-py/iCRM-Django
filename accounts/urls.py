from django.urls import path
from . import views

urlpatterns = [
    path('invoices', views.invoices, name='invoices'),
    path('<int:id>', views.reciept, name='invoice'),
    path('quotation', views.quotation, name='quotation'),
]