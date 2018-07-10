from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .serializers import PizzaSerializer
from .models import Pizza


class PizzaViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = Pizza.objects.all()
    serializer_class = PizzaSerializer
    permission_classes = [AllowAny]
