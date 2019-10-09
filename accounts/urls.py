from django.urls import path
from . import views

urlpatterns = [
    path('invoices', views.invoices, name='invoices'),
    path('<int:id>', views.lead_invoice, name='invoice'),
    path('bill/<int:id>', views.each_bill, name='lead_bill'),
    path('quotation', views.quotation, name='quotation'),
]