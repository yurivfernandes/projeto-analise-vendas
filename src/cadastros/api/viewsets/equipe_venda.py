from rest_framework.viewsets import ModelViewSet

from ...models import EquipeVenda
from ..serializers import EquipeVendaSerializer


class EquipeVendaViewset(ModelViewSet):
    serializer_class = EquipeVendaSerializer
    queryset = EquipeVenda.objects.all()
    pagination_class = None
