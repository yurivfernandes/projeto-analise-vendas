from django.db import models
from django.db.models import F, Value
from django.db.models.functions import Concat

from .fornecedor import Fornecedor
from .grupo_produto import GrupoProduto


class ProdutoQuerySet(models.QuerySet):
    """Classe que customiza o QuerySet da model principal"""

    def annotate_with_grupo_produto_and_fornecedor_related(
        self,
    ) -> models.QuerySet:
        """Retorna um queryset com dados relacionados ao Produto"""
        return self.select_related("grupo_produto", "fornecedor").annotate(
            grupo_produto__label=Concat(
                F("grupo_produto__codigo"),
                Value(" | "),
                F("grupo_produto__nome"),
            ),
            fornecedor__label=Concat(
                F("fornecedor__cnpj"), Value(" | "), F("fornecedor__nome")
            ),
        )


class Produto(models.Model):
    nome = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, unique=True)
    custo = models.DecimalField(max_digits=14, decimal_places=2)
    grupo_produto = models.ForeignKey(
        GrupoProduto,
        on_delete=models.CASCADE,
        related_name="cadastros_produto_set",
    )
    fornecedor = models.ForeignKey(
        Fornecedor,
        on_delete=models.CASCADE,
        related_name="cadastros_produto_set",
    )
    sku = models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = ProdutoQuerySet.as_manager()

    class Meta:
        db_table = "cadastro_produto"
        verbose_name = "Cadastros de Produto"
        verbose_name_plural = "Cadastros de Produtos"
        unique_together = ("nome", "codigo")
