from unittest.mock import patch

import pytest
from rest_framework.test import APIClient


@pytest.fixture
def client():
    return APIClient()


class TestInvoiceListView:
    URL = "/api/invoices/"

    def test_returns_400_when_dates_missing(self, client):
        response = client.get(self.URL)

        assert response.status_code == 400
        assert "start_date" in response.json()["error"]

    def test_returns_400_when_only_start_date_provided(self, client):
        response = client.get(self.URL, {"start_date": "2022-01-01"})

        assert response.status_code == 400

    def test_returns_400_when_only_end_date_provided(self, client):
        response = client.get(self.URL, {"end_date": "2022-01-31"})

        assert response.status_code == 400

    def test_returns_400_when_date_format_invalid(self, client):
        response = client.get(
            self.URL, {"start_date": "01-01-2022", "end_date": "31-01-2022"}
        )

        assert response.status_code == 400
        assert "format" in response.json()["error"].lower()

    def test_returns_400_when_start_date_greater_than_end_date(self, client):
        response = client.get(
            self.URL, {"start_date": "2022-02-01", "end_date": "2022-01-01"}
        )

        assert response.status_code == 400
        assert "greater" in response.json()["error"].lower()

    @patch("apps.invoices.api.views.get_invoices_by_date_range")
    def test_returns_200_with_paginated_response(
        self, mock_service, client, sample_invoices
    ):
        mock_service.return_value = sample_invoices

        response = client.get(
            self.URL, {"start_date": "2022-01-01", "end_date": "2022-01-31"}
        )

        assert response.status_code == 200
        body = response.json()
        assert "count" in body
        assert "next" in body
        assert "previous" in body
        assert "results" in body

    @patch("apps.invoices.api.views.get_invoices_by_date_range")
    def test_results_contain_expected_fields(
        self, mock_service, client, sample_invoices
    ):
        mock_service.return_value = sample_invoices

        response = client.get(
            self.URL, {"start_date": "2022-01-01", "end_date": "2022-01-31"}
        )

        first_result = response.json()["results"][0]
        assert set(first_result.keys()) == {
            "id",
            "invoice_number",
            "total",
            "invoice_date",
            "status",
        }
