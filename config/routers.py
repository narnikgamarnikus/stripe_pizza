from rest_framework import routers
from stripe_pizza.customers.views import CustomerViewSet
from stripe_pizza.orders.views import OrderViewSet
from stripe_pizza.pizzas.views import PizzaViewSet

router = routers.SimpleRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'pizzas', PizzaViewSet)
