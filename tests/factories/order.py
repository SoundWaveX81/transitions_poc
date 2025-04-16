import factory
from datetime import datetime


class BasicOrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "order.Order"

    start_date = str(datetime.now().date())
