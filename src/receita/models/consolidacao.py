from django.db import models
from django.db.models import F, Value
from django.db.models.functions import Concat

from cadastros.models import Produto, Vendedor

from .tipo import Tipo


class ConsolidacaoQuerySet(models.QuerySet):
    """Classe que customiza o QuerySet da model principal"""

    def annotate_with_vendedor_related(self) -> models.QuerySet:
        """Retorna um queryset com dados relacionados ao Vendedor"""
        return (
            self
            .select_related('vendedor')
            .annotate(
                vendedor__label=Concat(
                    F('vendedor__codigo'),
                    Value(' | '),
                    F('vendedor__nome')),
                equipe_venda__label=Concat(
                    F('vendedor__equipe_venda__codigo'),
                    Value(' | '),
                    F('vendedor__equipe_venda__nome')),
                loja__label=Concat(
                    F('vendedor__equipe_venda__loja__codigo'),
                    Value(' | '),
                    F('vendedor__equipe_venda__loja__nome'))
            )
        )

    def annotate_with_produto_related(self) -> models.QuerySet:
        """Retorna um queryset com dados relacionados ao Produto"""
        return (
            self
            .select_related('produto')
            .annotate(
                produto__label=Concat(
                    F('produto__codigo'),
                    Value(' | '),
                    F('produto__nome')),
                grupo_produto__label=Concat(
                    F('produto__grupo_produto__codigo'),
                    Value(' | '),
                    F('produto__grupo_produto__nome')),
                fornecedor__label=Concat(
                    F('produto__fornecedor__cnpj'),
                    Value(' | '),
                    F('produto__fornecedor__nome'))
            )
        )


class Consolidacao(models.Model):
    data = models.DateField()
    valor = models.DecimalField(max_digits=14, decimal_places=2)
    tipo = models.ForeignKey(
        Tipo, on_delete=models.CASCADE, related_name='receita_consolidacao_set')
    vendedor = models.ForeignKey(
        Vendedor, on_delete=models.CASCADE, related_name='receita_consolidacao_set')
    produto = models.ForeignKey(
        Produto, on_delete=models.CASCADE, related_name='receita_consolidacao_set')
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ConsolidacaoQuerySet.as_manager()

    class Meta:
        db_table = 'receita_consolidacao'
        verbose_name = 'Receita Consolidação'
        verbose_name_plural = 'Consolidação de Receita'
