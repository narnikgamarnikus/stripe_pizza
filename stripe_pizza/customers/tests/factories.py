from factory import DjangoModelFactory, Faker

from ..models import Customer


class CustomerFactory(DjangoModelFactory):

    first_name = Faker("first_name")
    last_name = Faker("last_name")
    email = Faker("email")
    address = Faker("address")

    class Meta:
        model = Customer
