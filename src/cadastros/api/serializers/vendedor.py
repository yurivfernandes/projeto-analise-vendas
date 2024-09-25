from rest_framework.serializers import ModelSerializer

from ...models import Vendedor


class VendedorSerializer(ModelSerializer):
    class Meta:
        model = Vendedor
        fields = (
            "id",
            "nome",
            "codigo",
            "equipe_venda_id"
        )
