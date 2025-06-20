from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from produce.serializers import FarmProduceSerializer
from .models import FarmProduce

class ProductModalViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FarmProduce.objects.all()
    serializer_class = FarmProduceSerializer