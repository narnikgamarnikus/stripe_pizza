from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Customer


@receiver(post_save, sender=Customer)
def handle_customer_post_save(sender, created, instance, **kwargs):
    pass
