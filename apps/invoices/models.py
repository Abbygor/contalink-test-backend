from django.db import models


# Create your models here.
class Invoice(models.Model):
    invoice_number = models.CharField(max_length=255, null=True)
    total = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    invoice_date = models.DateTimeField(null=True)
    status = models.CharField(max_length=255, null=True)
    active = models.BooleanField()

    class Meta:
        managed = False
        db_table = "invoices"
