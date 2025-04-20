from decimal import Decimal

from django.db import models

from apps.common.models import CommonData
from apps.status_machine.models import OrderStatus


class Order(CommonData):
    ready_to_customer = models.BooleanField(default=False)
    signed = models.BooleanField(default=False)
    start_date = models.DateField(verbose_name="Order start date", null=True)
    status = models.ForeignKey(OrderStatus, on_delete=models.DO_NOTHING, default=1)
    snapshot = models.JSONField(blank=True, null=True, default=dict)

    @property
    def total_price(self):
        if not self.snapshot or "orderlines" not in self.snapshot:
            return Decimal(0.00)

        orderlines = self.snapshot["orderlines"]
        total: Decimal = Decimal(0.00)

        for line in orderlines:
            if line:
                total += Decimal(line["product"]["price"])

        return total

    def __str__(self):
        return f"{self.id} - {self.status.description}"

    class Meta:
        db_table = "order"
