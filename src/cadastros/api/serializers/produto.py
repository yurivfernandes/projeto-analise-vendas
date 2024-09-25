from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from ...models import Produto


class ProdutoSerializer(ModelSerializer):
    grupo_produto_label = CharField(
        source="grupo_produto__label", read_only=True
    )
    fornecedor_label = CharField(source="fornecedor__label", read_only=True)

    class Meta:
        model = Produto
        fields = (
            "id",
            "nome",
            "codigo",
            "custo",
            "sku",
            "grupo_produto_label",
            "fornecedor_label",
        )
