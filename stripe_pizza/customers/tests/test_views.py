import pytest

from django.urls import reverse

from rest_framework.test import APIRequestFactory

from stripe_pizza.customers.views import CustomerViewSet
from .factories import CustomerFactory


pytestmark = pytest.mark.django_db
factory = APIRequestFactory()


class TestCostoremListView:

    def test_list_without_customer(self):
        view = CustomerViewSet.as_view(actions={'get': 'list'})
        request = factory.get(
            reverse('customer-list')
        )
        response = view(request)
        assert response.data == []
        assert response.status_code == 200

    def test_list_with_customer(self):
        CustomerFactory()
        view = CustomerViewSet.as_view(actions={'get': 'list'})
        request = factory.get(
            reverse('customer-list')
        )
        response = view(request)
        assert 'first_name' in response.data[0]
        assert 'last_name' in response.data[0]
        assert 'email' in response.data[0]
        assert 'address' in response.data[0]
        assert response.status_code == 200

    def test_create_without_customer(self):
        view = CustomerViewSet.as_view(actions={'post': 'create'})
        request = factory.post(
            reverse('customer-list'),
        )
        response = view(request)
        assert response.status_code == 400

    def test_create_with_customer(self):
        data = {
            'first_name': 'Joe',
            'last_name': 'Doe',
            'address': '02092 Stone StationPort Daniel, IL 53803-9882',
            'email': 'joedoe@gmail.com'
        }
        view = CustomerViewSet.as_view(actions={'post': 'create'})
        request = factory.post(
            reverse('customer-list'),
            data
        )
        response = view(request)
        assert response.status_code == 201

        assert response.data['first_name'] == data['first_name']
        assert response.data['last_name'] == data['last_name']
        assert response.data['address'] == data['address']
        assert response.data['email'] == data['email']


class TestCustomerDetailView:

    def test_retrieve_without_customer(self):
        view = CustomerViewSet.as_view(actions={'get': 'retrieve'})
        response = view(factory.get(""), pk=1)
        assert response.status_code == 404

    def test_retrieve_with_customer(self):
        customer = CustomerFactory()
        view = CustomerViewSet.as_view(actions={'get': 'retrieve'})
        response = view(factory.get(""), pk=customer.pk)
        assert response.status_code == 200
        assert 'first_name' in response.data
        assert 'last_name' in response.data
        assert 'address' in response.data
        assert 'email' in response.data

    def test_partial_update_without_customer(self):
        view = CustomerViewSet.as_view(actions={'patch': 'partial_update'})
        response = view(factory.patch(""), pk=1)
        assert response.status_code == 404

    def test_partial_update_customer_address(self):
        data = {'address': 'FAKE ADDRESS'}
        customer = CustomerFactory()
        view = CustomerViewSet.as_view(actions={'patch': 'partial_update'})
        response = view(
            factory.patch(
                "",
                data
            ),
            pk=customer.pk
        )
        assert response.status_code == 200
        assert response.data['address'] == 'FAKE ADDRESS'

    def test_update_without_customer(self):
        view = CustomerViewSet.as_view(actions={'put': 'update'})
        response = view(factory.put(""), pk=1)
        assert response.status_code == 404

    def test_update_with_customer(self):
        data = {
            'first_name': 'Joe',
            'last_name': 'Doe',
            'address': '02092 Stone StationPort Daniel, IL 53803-9882',
            'email': 'joedoe@gmail.com'
        }
        customer = CustomerFactory()
        view = CustomerViewSet.as_view(actions={'put': 'update'})
        response = view(
            factory.put(
                "",
                data
            ),
            pk=customer.pk
        )
        assert response.status_code == 200
        assert response.data['first_name'] == data['first_name']
        assert response.data['last_name'] == data['last_name']
        assert response.data['address'] == data['address']
        assert response.data['email'] == data['email']

    def test_destroy_without_customer(self):
        view = CustomerViewSet.as_view(actions={'delete': 'destroy'})
        response = view(factory.delete(""), pk=1)
        assert response.status_code == 404

    def test_destroy_with_customer(self):
        customer = CustomerFactory()
        view = CustomerViewSet.as_view(actions={'delete': 'destroy'})
        response = view(
            factory.delete(
                ""
            ),
            pk=customer.pk
        )
        assert response.data is None
        assert response.status_code == 204
