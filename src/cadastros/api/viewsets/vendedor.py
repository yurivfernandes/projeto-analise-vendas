from rest_framework.viewsets import ModelViewSet

from ...models import Vendedor
from ..serializers import VendedorSerializer


class VendedorViewset(ModelViewSet):
    serializer_class = VendedorSerializer
    queryset = Vendedor.objects.all()
    pagination_class = None
