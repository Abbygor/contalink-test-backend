from decimal import Decimal
from unittest.mock import patch

from apps.invoices.tasks import send_top_10_invoices_email


class TestSendTop10InvoicesEmail:
    @patch("apps.invoices.tasks.send_mail")
    @patch("apps.invoices.tasks.get_top_selling_days")
    def test_calls_top_selling_days_service(self, mock_service, mock_send_mail):
        mock_service.return_value = []

        send_top_10_invoices_email()

        mock_service.assert_called_once()

    @patch("apps.invoices.tasks.send_mail")
    @patch("apps.invoices.tasks.get_top_selling_days")
    def test_sends_email_with_subject_and_recipients(
        self, mock_service, mock_send_mail
    ):
        mock_service.return_value = []

        send_top_10_invoices_email()

        mock_send_mail.assert_called_once()
        call_kwargs = mock_send_mail.call_args.kwargs
        assert call_kwargs["subject"] == "Daily Top 10 Sales Report"
        assert call_kwargs["fail_silently"] is False

    @patch("apps.invoices.tasks.send_mail")
    @patch("apps.invoices.tasks.get_top_selling_days")
    def test_email_body_contains_top_days(self, mock_service, mock_send_mail):
        mock_service.return_value = [
            {"day": "2026-02-06", "total": Decimal("940220.00")},
            {"day": "2026-02-02", "total": Decimal("513358.00")},
        ]

        send_top_10_invoices_email()

        body = mock_send_mail.call_args.kwargs["message"]
        assert "2026-02-06: $940220.00" in body
        assert "2026-02-02: $513358.00" in body
