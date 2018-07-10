import pytest

from django.urls import reverse

from rest_framework.test import APIRequestFactory

from ..views import PizzaViewSet
from .factories import PizzaFactory


pytestmark = pytest.mark.django_db
factory = APIRequestFactory()


class TestPizzaListView:

    def test_list_without_pizzas(self):
        view = PizzaViewSet.as_view(actions={'get': 'list'})
        request = factory.get(
            reverse('pizza-list')
        )
        response = view(request)
        assert response.data == []
        assert response.status_code == 200

    def test_list_with_pizzas(self):
        PizzaFactory()
        view = PizzaViewSet.as_view(actions={'get': 'list'})
        request = factory.get(
            reverse('pizza-list')
        )
        response = view(request)
        assert 'size' in response.data[0]
        assert len(response.data) == 1
        assert response.status_code == 200

    def test_create_without_pizza_data(self):
        view = PizzaViewSet.as_view(actions={'post': 'create'})
        request = factory.post(
            reverse('pizza-list'),
        )
        response = view(request)
        assert response.status_code == 400

    def test_create_with_invalid_pizza_data(self):
        data = {
            'size': 'INVALID PIZZA SIZE',
        }
        view = PizzaViewSet.as_view(actions={'post': 'create'})
        request = factory.post(
            reverse('pizza-list'),
            data
        )
        response = view(request)
        assert response.status_code == 400

    def test_create_with_valid_pizza_data(self):
        data = {
            'size': 'fifty',
        }
        view = PizzaViewSet.as_view(actions={'post': 'create'})
        request = factory.post(
            reverse('pizza-list'),
            data
        )
        response = view(request)
        assert response.status_code == 201
        assert response.data['size'] == 'fifty'


class TestCustomerDetailView:

    def test_retrieve_without_customer(self):
        view = PizzaViewSet.as_view(actions={'get': 'retrieve'})
        response = view(factory.get(""), pk=1)
        assert response.status_code == 404

    def test_retrieve_with_customer(self):
        customer = PizzaFactory()
        view = PizzaViewSet.as_view(actions={'get': 'retrieve'})
        response = view(factory.get(""), pk=customer.pk)
        assert response.status_code == 200
        assert 'size' in response.data

    def test_partial_update_without_customer(self):
        view = PizzaViewSet.as_view(actions={'patch': 'partial_update'})
        response = view(factory.patch(""), pk=1)
        assert response.status_code == 404

    def test_partial_update_pizza(self):
        data = {'size': 'fifty'}
        customer = PizzaFactory()
        view = PizzaViewSet.as_view(actions={'patch': 'partial_update'})
        response = view(
            factory.patch(
                "",
                data
            ),
            pk=customer.pk
        )
        assert response.status_code == 200
        assert 'size' in response.data
        assert response.data['size'] == 'fifty'

    def test_update_without_pizza(self):
        view = PizzaViewSet.as_view(actions={'put': 'update'})
        response = view(factory.put(""), pk=1)
        assert response.status_code == 404

    def test_update_with_pizza(self):
        data = {'size': 'fifty'}
        customer = PizzaFactory()
        view = PizzaViewSet.as_view(actions={'put': 'update'})
        response = view(
            factory.put(
                "",
                data
            ),
            pk=customer.pk
        )
        assert response.status_code == 200
        assert response.data['size'] == data['size']

    def test_destroy_without_customer(self):
        view = PizzaViewSet.as_view(actions={'delete': 'destroy'})
        response = view(factory.delete(""), pk=1)
        assert response.status_code == 404

    def test_destroy_with_customer(self):
        customer = PizzaFactory()
        view = PizzaViewSet.as_view(actions={'delete': 'destroy'})
        response = view(
            factory.delete(
                ""
            ),
            pk=customer.pk
        )
        assert response.data is None
        assert response.status_code == 204
