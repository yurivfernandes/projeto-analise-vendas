from rest_framework.viewsets import ModelViewSet

from ...models import Produto
from ..serializers import ProdutoSerializer


class ProdutoViewset(ModelViewSet):
    serializer_class = ProdutoSerializer
    queryset = Produto.objects.annotate_with_grupo_produto_and_fornecedor_related()
    pagination_class = None
