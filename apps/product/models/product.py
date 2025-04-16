from apps.common.models import CommonData
from .product_type import ProductType

from django.db import models


class Product(CommonData):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=300)
    product_type = models.ForeignKey(ProductType, on_delete=models.PROTECT)
    basic_price = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        db_table = "product"
