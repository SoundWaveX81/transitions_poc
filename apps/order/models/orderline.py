from django.db import models, transaction

from apps.common.models import CommonData
from apps.product.models import Product

from .order import Order


class OrderLine(CommonData):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="orderlines")

    def __str__(self):
        return f"{self.id} {self.created_at} / {self.order} / {self.product}"

    class Meta:
        db_table = "order_line"

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)

            order = self.order
            if not order.snapshot:
                order.snapshot = {"orderlines": []}

            line_data = {
                "id": self.id,
                "product": {
                    "id": self.product.id,
                    "name": self.product.name,
                    "price": str(self.product.basic_price),
                },
                "timestamp": str(self.created_at),
            }

            order.snapshot["orderlines"].append(line_data)
            order.save(update_fields=["snapshot"])
