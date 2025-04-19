__all__ = [
    "validate_CREATED_to_DRAFT",
]


import typing

from django.core.exceptions import ValidationError

if typing.TYPE_CHECKING:
    from order.models import Order


def validate_CREATED_to_DRAFT(order: "Order") -> None:
    if not order.orderlines.exists():
        raise ValidationError(f"Order {order.id} cannot be moved to draft, it does not have any orderline")

    if "orderlines" not in order.snapshot:
        raise ValidationError(f"Order {order.id} cannot be moved to draft, orderlines snapshot cannot be empty")

    if order.signed:
        raise ValidationError(f"Order {order.id} cannot be moved to draft, signed field must be empty")
