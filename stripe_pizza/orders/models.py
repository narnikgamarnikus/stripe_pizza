from django.db import models
from django.conf import settings

import stripe

API_KEY = settings.STRIPE_API_KEY
stripe.api_key = API_KEY


class Order(models.Model):

    pizza = models.ForeignKey(
        'pizzas.Pizza',
        on_delete=models.CASCADE
    )

    customer = models.ForeignKey(
        'customers.Customer',
        on_delete=models.CASCADE,
        related_name='orders'
    )

    stripe_id = models.CharField(max_length=25, null=True, default='')

    def save(self, *args, **kwargs):
        if not self.pk:
            order = stripe.Order.create(
                currency='usd',
                customer=self.customer.stripe_id
            )
            self.stripe_id = order['id']
        return super(Order, self).save(*args, **kwargs)
