from rest_framework.serializers import ModelSerializer

from ...models import Consolidacao


class ConsolidacaoSerializer(ModelSerializer):
    class Meta:
        model = Consolidacao
        fields = (
            "id",
            "data",
            "valor",
            "produto_id",
            "tipo_id",
            "vendedor_id",
        )
