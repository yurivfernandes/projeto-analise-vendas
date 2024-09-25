from rest_framework.serializers import ModelSerializer

from ...models import EquipeVenda


class EquipeVendaSerializer(ModelSerializer):
    class Meta:
        model = EquipeVenda
        fields = (
            "id",
            "codigo",
            "nome",
            "loja_id",
            "percent_comissao"
        )
