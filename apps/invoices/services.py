from datetime import datetime

from django.db.models import Sum
from django.db.models.functions import TruncDate

from apps.invoices.models import Invoice


def get_invoices_by_date_range(start_date: datetime, end_date: datetime):
    return Invoice.objects.filter(
        invoice_date__gte=start_date,
        invoice_date__lte=end_date,
        active=True,
    ).order_by("-invoice_date")


def get_top_selling_days(limit: int = 10):
    return (
        Invoice.objects.filter(active=True, status="Vigente")
        .annotate(day=TruncDate("invoice_date"))
        .values("day")
        .annotate(total=Sum("total"))
        .order_by("-total")[:limit]
    )
