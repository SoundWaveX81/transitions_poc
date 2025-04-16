from django.db import models


class OrderStatus(models.Model):
    code = models.IntegerField(verbose_name="Status code")
    description = models.CharField(verbose_name="description")

    def __str__(self):
        return f"{self.code} - {self.description}"

    class Meta:
        ordering = ["code"]
        db_table = "order_status"
        verbose_name_plural = "order statuses"
