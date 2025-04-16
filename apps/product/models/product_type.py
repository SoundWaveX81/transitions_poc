from django.db import models

from apps.common.models import CommonData


class ProductType(CommonData):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=150)
    source = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        db_table = "product_type"
