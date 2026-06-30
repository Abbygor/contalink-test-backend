from datetime import datetime
from decimal import Decimal

import pytest

from apps.invoices.models import Invoice


@pytest.fixture
def sample_invoices():
    return [
        Invoice(
            id=1,
            invoice_number="C30001",
            total=Decimal("100.00"),
            invoice_date=datetime(2022, 1, 10, 12, 0, 0),
            status="Vigente",
            active=True,
        ),
        Invoice(
            id=2,
            invoice_number="C30002",
            total=Decimal("250.50"),
            invoice_date=datetime(2022, 1, 15, 9, 30, 0),
            status="Vigente",
            active=True,
        ),
        Invoice(
            id=3,
            invoice_number="C30003",
            total=Decimal("75.25"),
            invoice_date=datetime(2022, 2, 1, 18, 45, 0),
            status="Cancelada",
            active=False,
        ),
    ]
