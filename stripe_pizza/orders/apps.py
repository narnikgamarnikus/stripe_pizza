from django.apps import AppConfig


class OrdersAppConfig(AppConfig):

    name = "stripe_pizza.orders"
    verbose_name = "Orders"

    def ready(self):
        try:
            import stripe_pizza.orders.receivers
        except ImportError:
            pass
