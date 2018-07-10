from django.db import models
from django.conf import settings

import stripe

API_KEY = settings.STRIPE_API_KEY
stripe.api_key = API_KEY


class Customer(models.Model):

    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    address = models.CharField(max_length=250)

    stripe_id = models.CharField(max_length=25, null=True, default='')

    @property
    def full_name(self):
        return '{} {}'.format(
            self.first_name,
            self.last_name
        )

    def save(self, *args, **kwargs):
        if not self.pk:
            stripe_customer = stripe.Customer.create(
                email=self.email,
            )
            self.stripe_id = stripe_customer['id']
        return super(Customer, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        stripe.Customer.update(
            email=self.email
        )
        return super(Customer, self).update(*args, **kwargs)
