import factory
from faker import Faker

from tests.factories.order import BasicOrderFactory
from tests.factories.product import ProductFactory

faker = Faker()


class OrderLineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "order.OrderLine"

    order = factory.SubFactory(BasicOrderFactory)
    product = factory.SubFactory(ProductFactory)
