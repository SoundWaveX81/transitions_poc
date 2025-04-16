import datetime

from django.db import models


class CommonData(models.Model):
    created_at: datetime = models.DateTimeField("created", auto_now_add=True)
    updated_at: datetime = models.DateTimeField("updated", auto_now=True)

    class Meta:
        abstract = True
