import pytest

from ..serializers import PizzaSerializer
from .factories import PizzaFactory

from stripe_pizza.pizzas.models import Pizza

pytestmark = pytest.mark.django_db


class TestPizzaSerializer:

    def test_serializer_with_empty_data(self):
        serializer = PizzaSerializer(data={})
        assert serializer.is_valid() is False

    def test_serializer_with_valid_data(self):
        pizza = PizzaFactory()
        serializer = PizzaSerializer(pizza)
        pizza = Pizza.objects.first()
        pizza.delete()
        serializer = PizzaSerializer(data=serializer.data)
        assert serializer.is_valid() is True
