from django.test import TestCase
from tests.factories.order import BasicOrderFactory
from tests.factories.orderline import OrderLineFactory
from tests.factories.product import ProductFactory

from apps.order.models import OrderLine


class OrderLineModelTest(TestCase):
    fixtures = ("apps/status_machine/fixtures/orderstatus.fixture.json",)

    def setUp(self):
        self.order = BasicOrderFactory()

    def test_create_orderline_snapshot_on_order_ok(self):
        orderline = OrderLine(product=ProductFactory(), order=self.order)
        orderline.save()
        self.assertIn("orderlines", self.order.snapshot)
        self.assertEqual(str(orderline.product.basic_price), self.order.snapshot["orderlines"][0]["product"]["price"])

    def test_multiple_orderlines_values_sum_on_order_snapshot_ok(self):
        orderlines = OrderLineFactory.create_batch(3, order=self.order)
        expected_total_price = 0
        for line in orderlines:
            expected_total_price += line.product.basic_price

        self.assertEqual(expected_total_price, self.order.total_price)

    def test_remove_orderline_from_snapshot_on_orderline_delete_ok(self):
        orderlines_qty = 5
        orderlines = OrderLineFactory.create_batch(orderlines_qty, order=self.order)

        self.assertEqual(orderlines_qty, len(self.order.snapshot["orderlines"]))

        orderlines[2].delete()
        self.order.refresh_from_db()

        self.assertEqual(self.order.orderlines.all().count(), orderlines_qty - 1)
        self.assertEqual(orderlines_qty - 1, len(self.order.snapshot["orderlines"]))
        self.assertEqual(self.order.orderlines.all()[0].id, self.order.snapshot["orderlines"][0]["id"])
