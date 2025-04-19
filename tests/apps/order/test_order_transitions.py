from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.status_machine.constants import OrderStatuses
from apps.status_machine.services import OrderStatusMachine
from tests.factories.orderline import BasicOrderFactory, OrderLineFactory


class OrderTransitionsTest(TestCase):
    fixtures = ("apps/status_machine/fixtures/orderstatus.fixture.json",)

    def setUp(self):
        self.orderline = OrderLineFactory()
        self.order_to_fail = BasicOrderFactory()

    def test_transition_from_created_to_draft_ok(self):
        """
        test that the order can be moved from created to draft.
        Contitions:
        - order has to have at least one orderline
        - order cannot have empty 'orderlines' attribute on snapshot field
        - order cannot be in draft if the signed field is True

        other scenarios
        - if the orderlines are removed the order has to back to created status
        """
        self.assertEqual(self.orderline.order.status.code, OrderStatuses.CREATED.value)
        status_machine = OrderStatusMachine(self.orderline.order)
        status_machine.transition(OrderStatuses.DRAFT.value)

        self.assertEqual(self.orderline.order.status.code, OrderStatuses.DRAFT.value)

    def test_transition_from_created_to_draft_no_orderlines_ko(self):
        self.assertFalse(self.order_to_fail.orderlines.exists())
        status_machine = OrderStatusMachine(self.order_to_fail)

        with self.assertRaises(ValidationError) as err:
            status_machine.transition(OrderStatuses.DRAFT.value)

        self.assertEqual(
            f"Order {self.order_to_fail.id} cannot be moved to draft, it does not have any orderline",
            err.exception.message,
        )

    def test_transition_from_created_to_draft_empty_snapshot_ko(self):
        self.orderline.order.snapshot = {}
        self.assertFalse("orderlines" in self.order_to_fail.snapshot)
        status_machine = OrderStatusMachine(self.orderline.order)

        with self.assertRaises(ValidationError) as err:
            status_machine.transition(OrderStatuses.DRAFT.value)

        self.assertEqual(
            f"Order {self.orderline.order.id} cannot be moved to draft, orderlines snapshot cannot be empty",
            err.exception.message,
        )

    def test_transition_from_created_to_draft_signed_true_ko(self):
        self.orderline.order.signed = True
        self.assertFalse("orderlines" in self.order_to_fail.snapshot)
        status_machine = OrderStatusMachine(self.orderline.order)

        with self.assertRaises(ValidationError) as err:
            status_machine.transition(OrderStatuses.DRAFT.value)

        self.assertEqual(
            f"Order {self.orderline.order.id} cannot be moved to draft, signed field must be empty",
            err.exception.message,
        )
