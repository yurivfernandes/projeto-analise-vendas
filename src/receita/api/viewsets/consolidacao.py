from rest_framework.viewsets import ModelViewSet

from app.paginators import CustomLargePagination

from ...models import Consolidacao
from ..serializers import ConsolidacaoSerializer


class ConsolidacaoViewset(ModelViewSet):
    serializer_class = ConsolidacaoSerializer
    queryset = Consolidacao.objects.all()
    pagination_class = CustomLargePagination
