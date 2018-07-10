import pytest

from django.urls import reverse

from rest_framework.test import APIRequestFactory

from stripe_pizza.pizzas.models import Pizza
from stripe_pizza.pizzas.tests.factories import PizzaFactory
from stripe_pizza.customers.tests.factories import CustomerFactory
from stripe_pizza.orders.views import OrderViewSet
from .factories import OrderFactory


pytestmark = pytest.mark.django_db
factory = APIRequestFactory()


class TestOrderListView:

    def test_list_without_order(self):
        view = OrderViewSet.as_view(actions={'get': 'list'})
        request = factory.get(reverse('order-list'))
        response = view(request)
        assert response.data == []
        assert response.status_code == 200

    def test_list_with_order(self):
        OrderFactory()
        view = OrderViewSet.as_view(actions={'get': 'list'})
        request = factory.get(reverse('order-list'))
        response = view(request)
        assert 'customer' in response.data[0]
        assert 'pizza' in response.data[0]
        assert response.status_code == 200

    def test_create_without_order(self):
        view = OrderViewSet.as_view(actions={'post': 'create'})
        request = factory.post(
            reverse('order-list'),
        )
        response = view(request)
        assert response.status_code == 400

    def test_create_with_order(self):
        pizza = PizzaFactory()
        customer = CustomerFactory()
        data = {
            'pizza': pizza.id,
            'customer': customer.id
        }
        view = OrderViewSet.as_view(actions={'post': 'create'})
        request = factory.post(
            reverse('customer-list'),
            data
        )
        response = view(request)
        assert response.status_code == 201

        assert 'pizza' in response.data
        assert 'customer' in response.data


class TestOrderDetailView:

    def test_retrieve_without_order(self):
        view = OrderViewSet.as_view(actions={'get': 'retrieve'})
        response = view(factory.get(""), pk=1)
        assert response.status_code == 404

    def test_retrieve_with_order(self):
        order = OrderFactory()
        view = OrderViewSet.as_view(actions={'get': 'retrieve'})
        response = view(factory.get(""), pk=order.pk)
        assert response.status_code == 200
        assert 'pizza' in response.data
        assert 'customer' in response.data

    def test_partial_update_without_order(self):
        view = OrderViewSet.as_view(actions={'patch': 'partial_update'})
        response = view(factory.patch(""), pk=1)
        assert response.status_code == 404

    def test_partial_update_order_pizza(self):
        order = OrderFactory()
        view = OrderViewSet.as_view(actions={'patch': 'partial_update'})
        pizza = PizzaFactory(size='thirty')
        data = {'pizza': pizza.id}
        response = view(
            factory.patch(
                "",
                data,
                format='json'
            ),
            pk=order.pk
        )
        assert response.status_code == 200
        assert response.data['pizza'] == pizza.id
        pizza = Pizza.objects.first()
        view = OrderViewSet.as_view(actions={'patch': 'partial_update'})
        data = {'pizza': pizza.id}
        response = view(
            factory.patch(
                "",
                data,
                format='json'
            ),
            pk=order.pk
        )
        assert response.status_code == 200
        assert response.data['pizza'] == pizza.id

    def test_partial_update_order_customer(self):
        order = OrderFactory()
        view = OrderViewSet.as_view(actions={'patch': 'partial_update'})
        customer = CustomerFactory()
        data = {'customer': customer.id}
        response = view(
            factory.patch(
                "",
                data,
                format='json'
            ),
            pk=order.pk
        )
        assert response.status_code == 200
        assert response.data['customer'] == customer.id

        customer = CustomerFactory()
        view = OrderViewSet.as_view(actions={'patch': 'partial_update'})
        data = {'customer': customer.id}
        response = view(
            factory.patch(
                "",
                data,
                format='json'
            ),
            pk=order.pk
        )
        assert response.status_code == 200
        assert response.data['customer'] == customer.id

    def test_update_without_pizza(self):
        view = OrderViewSet.as_view(actions={'put': 'update'})
        response = view(factory.put(""), pk=1)
        assert response.status_code == 404

    def test_update_with_data(self):
        order = OrderFactory()
        customer = CustomerFactory()
        pizza = PizzaFactory(size='fifty')
        data = {
            'pizza': pizza.id,
            'customer': customer.id
        }
        view = OrderViewSet.as_view(actions={'put': 'update'})
        response = view(
            factory.put(
                "",
                data
            ),
            pk=order.pk
        )
        assert response.status_code == 200
        assert response.data['customer'] == customer.id

    def test_destroy_without_customer(self):
        view = OrderViewSet.as_view(actions={'delete': 'destroy'})
        response = view(factory.delete(""), pk=1)
        assert response.status_code == 404

    def test_destroy_with_customer(self):
        customer = OrderFactory()
        view = OrderViewSet.as_view(actions={'delete': 'destroy'})
        response = view(
            factory.delete(
                ""
            ),
            pk=customer.pk
        )
        assert response.data is None
        assert response.status_code == 204
