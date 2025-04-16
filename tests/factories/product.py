import factory
from factory.fuzzy import FuzzyDecimal
from faker import Faker

faker = Faker()


class ProductTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "product.ProductType"

    code = factory.Sequence(lambda n: f"TPT{n}")
    name = factory.LazyAttribute(lambda _: faker.word())
    description = "Test product type for testing"
    source = "STP"


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "product.Product"

    code = factory.Sequence(lambda n: f"TP{n}")
    name = factory.LazyAttribute(lambda _: faker.word())
    location = faker.address()
    product_type = factory.SubFactory(ProductTypeFactory)
    basic_price = FuzzyDecimal(300, 1200, precision=2)
