from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    fields = ('first_name', 'last_name', 'email', 'address')
