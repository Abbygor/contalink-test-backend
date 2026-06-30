from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from apps.invoices.services import get_top_selling_days


@shared_task
def send_top_10_invoices_email():
    top_days = get_top_selling_days()
    lines = [f"{row['day']}: ${row['total']}" for row in top_days]
    body = "Top 10 days with highest sales:\n\n" + "\n".join(lines)

    send_mail(
        subject="Daily Top 10 Sales Report",
        message=body,
        from_email=settings.EMAIL_FROM,
        recipient_list=[settings.EMAIL_TO],
        fail_silently=False,
    )
