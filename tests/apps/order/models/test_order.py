from datetime import datetime

from django.test import TestCase

from apps.order.models import Order


class OrderModelTest(TestCase):
    fixtures = ("apps/status_machine/fixtures/orderstatus.fixture.json",)

    def test_order_create_with_default_values_ok(self):
        order = Order(start_date=str(datetime.now().date()))
        order.save()

        self.assertFalse(order.signed)
        self.assertEqual(order.status.id, 1)
        self.assertEqual(order.snapshot, {})
