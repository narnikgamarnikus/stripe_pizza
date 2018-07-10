
import pytest

from ..serializers import OrderSerializer
from .factories import OrderFactory

pytestmark = pytest.mark.django_db


class TestOrderSerializer:

    def test_serializer_with_empty_data(self):
        serializer = OrderSerializer(data={})
        assert serializer.is_valid() is False

    def test_serializer_with_valid_data(self):
        order = OrderFactory()
        serializer = OrderSerializer(order)
        serializer = OrderSerializer(data=serializer.data)
        assert serializer.is_valid() is True
