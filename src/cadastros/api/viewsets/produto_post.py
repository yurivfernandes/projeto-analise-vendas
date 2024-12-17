from django.db.models import QuerySet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ...models import Produto
from ..serializers import ProdutoSerializer


class ProdutoPostViewset(ModelViewSet):
    serializer_class = ProdutoSerializer
    queryset = (
        Produto.objects.annotate_with_grupo_produto_and_fornecedor_related()
    )
    pagination_class = None

    @action(detail=False, methods=["post"])
    def get_produtos(self, request, *args, **kwargs):
        """
        Retorna o queryset de produtos em uma requisição POST.
        """
        queryset = self.queryset
        produto_id = request.data.get("produto_id", None)
        if produto_id != None:
            queryset = queryset.filter(id=produto_id)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
