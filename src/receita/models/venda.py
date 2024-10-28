from django.db import models
from django.db.models import F, Value
from django.db.models.functions import Concat

from cadastros.models import Cliente, Produto, Vendedor


class VendaQuerySet(models.QuerySet):
    """Classe que customiza o QuerySet da model principal"""

    def annotate_with_receita_bruta(self) -> models.QuerySet:
        return self.annotate(
            valor_receita_bruta=models.Sum("valor") * models.Sum("quantidade")
        )

    def annotate_with_vendedor_related(self) -> models.QuerySet:
        """Retorna um queryset com dados relacionados ao Vendedor"""
        return self.select_related("vendedor").annotate(
            vendedor__label=Concat(
                F("vendedor__codigo"), Value(" | "), F("vendedor__nome")
            ),
            equipe_venda__label=Concat(
                F("vendedor__equipe_venda__codigo"),
                Value(" | "),
                F("vendedor__equipe_venda__nome"),
            ),
            loja__label=Concat(
                F("vendedor__equipe_venda__loja__codigo"),
                Value(" | "),
                F("vendedor__equipe_venda__loja__nome"),
            ),
        )

    def annotate_with_produto_related(self) -> models.QuerySet:
        """Retorna um queryset com dados relacionados ao Produto"""
        return self.select_related("produto").annotate(
            produto__label=Concat(
                F("produto__codigo"), Value(" | "), F("produto__nome")
            ),
            grupo_produto__label=Concat(
                F("produto__grupo_produto__codigo"),
                Value(" | "),
                F("produto__grupo_produto__nome"),
            ),
            fornecedor__label=Concat(
                F("produto__fornecedor__cnpj"),
                Value(" | "),
                F("produto__fornecedor__nome"),
            ),
        )


class Venda(models.Model):
    data = models.DateField()
    nfe = models.CharField(max_length=10)
    valor = models.DecimalField(max_digits=14, decimal_places=2)
    produto = models.ForeignKey(
        Produto, on_delete=models.CASCADE, related_name="receita_venda_set"
    )
    vendedor = models.ForeignKey(
        Vendedor, on_delete=models.CASCADE, related_name="receita_venda_set"
    )
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, related_name="receita_venda_set"
    )
    quantidade = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = VendaQuerySet.as_manager()

    class Meta:
        db_table = "receita_venda"
        verbose_name = "Receita Venda"
        verbose_name_plural = "Receita Vendas"
