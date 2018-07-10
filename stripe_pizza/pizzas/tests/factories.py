from factory import DjangoModelFactory
from factory import fuzzy

from ..models import Pizza


class PizzaFactory(DjangoModelFactory):

    size = fuzzy.FuzzyChoice(['fifty', 'thirty'])

    class Meta:
        model = Pizza
