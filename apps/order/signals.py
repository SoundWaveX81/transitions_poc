from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.db import transaction

from apps.order.models import OrderLine


@receiver(post_delete, sender=OrderLine)
def update_order_snapshot_on_orderline_delete(sender, instance, **kwargs):
    order = instance.order
    orderlines_snapshot = order.snapshot.get("orderlines", [])
    new_snapshot = [line for line in orderlines_snapshot if line.get("id") != instance.id]
    order.snapshot["orderlines"] = new_snapshot

    with transaction.atomic():
        order.save(update_fields=["snapshot"])
