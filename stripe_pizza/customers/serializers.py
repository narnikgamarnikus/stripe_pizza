from rest_framework import serializers

from .models import Customer
from stripe_pizza.orders.serializers import OrderSerializer


class CustomerSerializer(serializers.ModelSerializer):

    orders = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        exclude = ['stripe_id']

    def get_orders(self, obj):
        serializer = OrderSerializer(obj.orders.all(), many=True)
        return serializer.data
