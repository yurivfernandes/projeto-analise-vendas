from rest_framework.serializers import ModelSerializer

from ...models import Loja


class LojaSerializer(ModelSerializer):
    class Meta:
        model = Loja
        fields = (
            "id",
            "nome",
            "codigo",
            "bairro",
            "cep",
            "cidade",
            "cnpj",
            "email",
            "rua",
            "telefone",
            "uf",
        )
