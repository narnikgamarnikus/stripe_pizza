from factory import DjangoModelFactory, SubFactory

from ..models import Order
from stripe_pizza.customers.tests.factories import CustomerFactory
from stripe_pizza.pizzas.tests.factories import PizzaFactory


class OrderFactory(DjangoModelFactory):

    customer = SubFactory(CustomerFactory)
    pizza = SubFactory(PizzaFactory)

    class Meta:
        model = Order
