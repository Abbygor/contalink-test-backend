from datetime import datetime
from unittest.mock import patch

from apps.invoices.services import (
    get_invoices_by_date_range,
    get_top_selling_days,
)


class TestGetInvoicesByDateRange:
    @patch("apps.invoices.services.Invoice.objects")
    def test_filters_by_date_range_and_active(self, mock_objects):
        start_date = datetime(2022, 1, 1)
        end_date = datetime(2022, 1, 31, 23, 59, 59)

        get_invoices_by_date_range(start_date, end_date)

        mock_objects.filter.assert_called_once_with(
            invoice_date__gte=start_date,
            invoice_date__lte=end_date,
            active=True,
        )

    @patch("apps.invoices.services.Invoice.objects")
    def test_orders_by_invoice_date_desc(self, mock_objects):
        start_date = datetime(2022, 1, 1)
        end_date = datetime(2022, 1, 31, 23, 59, 59)

        get_invoices_by_date_range(start_date, end_date)

        mock_objects.filter.return_value.order_by.assert_called_once_with(
            "-invoice_date"
        )


class TestGetTopSellingDays:
    @patch("apps.invoices.services.Invoice.objects")
    def test_filters_by_active_and_vigente(self, mock_objects):
        get_top_selling_days()

        mock_objects.filter.assert_called_once_with(active=True, status="Vigente")

    @patch("apps.invoices.services.Invoice.objects")
    def test_default_limit_is_10(self, mock_objects):
        get_top_selling_days()

        mock_objects.filter.return_value.annotate.return_value.values.return_value.annotate.return_value.order_by.return_value.__getitem__.assert_called_once_with(
            slice(None, 10, None)
        )

    @patch("apps.invoices.services.Invoice.objects")
    def test_custom_limit_is_respected(self, mock_objects):
        get_top_selling_days(limit=5)

        mock_objects.filter.return_value.annotate.return_value.values.return_value.annotate.return_value.order_by.return_value.__getitem__.assert_called_once_with(
            slice(None, 5, None)
        )
