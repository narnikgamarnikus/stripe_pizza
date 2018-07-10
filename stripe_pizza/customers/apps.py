from django.apps import AppConfig


class CustomersAppConfig(AppConfig):

    name = "stripe_pizza.customers"
    verbose_name = "Customers"

    def ready(self):
        try:
            import stripe_pizza.customers.receivers
        except ImportError:
            pass
