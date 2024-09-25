from rest_framework.viewsets import ModelViewSet

from ...models import Loja
from ..serializers import LojaSerializer


class LojaViewset(ModelViewSet):
    serializer_class = LojaSerializer
    queryset = Loja.objects.all()
    pagination_class = None
