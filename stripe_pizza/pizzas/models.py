from django.db import models
from django.conf import settings

from model_utils import Choices

import stripe

API_KEY = settings.STRIPE_API_KEY
stripe.api_key = API_KEY


class Pizza(models.Model):

    SIZES = Choices(
        ('thirty', '30cm'),
        ('fifty', '50cm')
    )

    size = models.CharField(
        choices=SIZES,
        max_length=6
    )
    SKU_id = models.CharField(
        max_length=25,
        null=True,
        unique=True
    )

    def __str__(self):
        return self.size

    def save(self, *args, **kwargs):
        if not self.pk:
            product = stripe.Product.create(
                name=self.__class__.__name__,
                type='good',
                description='{} of any size'.format(
                    self.__class__.__name__
                ),
                attributes=['size']
            )
            SKU = stripe.SKU.create(
                product=product['id'],
                attributes={
                    'size': self.size
                },
                price=100,
                currency='usd',
                inventory={
                    "type": "finite",
                    "quantity": 500
                }
            )
            self.SKU_id = SKU['id']
        return super(Pizza, self).save(*args, **kwargs)
