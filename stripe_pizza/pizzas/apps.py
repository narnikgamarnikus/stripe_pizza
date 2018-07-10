from django.apps import AppConfig


class PizzasAppConfig(AppConfig):

    name = "stripe_pizza.pizzas"
    verbose_name = "Pizzas"

    def ready(self):
        try:
            import stripe_pizza.pizzas.receivers
        except ImportError:
            pass
