from django.urls import path

from apps.invoices.api.views import InvoiceListView

urlpatterns = [path("invoices/", InvoiceListView.as_view(), name="invoice-list")]
