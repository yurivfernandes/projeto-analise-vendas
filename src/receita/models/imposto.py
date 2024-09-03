from django.db import models
from django.db.models import F, Value
from django.db.models.functions import Concat

from cadastros.models.loja import Loja

from .imposto_tipo import ImpostoTipo


class ImpostoQuerySet(models.QuerySet):
    """Classe que customiza o QuerySet da model principal"""

    def annotate_with_loja(self) -> models.QuerySet:
        """Retorna um queryset com dados relacionados à Loja"""
        return (
            self
            .select_related('loja')
            .annotate(
                loja__label=Concat(
                    F('loja__codigo'),
                    Value(' | '),
                    F('loja__nome'))
            )
        )


class Imposto(models.Model):
    percent = models.DecimalField(max_digits=5, decimal_places=2)
    loja = models.ForeignKey(
        Loja, on_delete=models.CASCADE, related_name='receita_imposto_set')
    tipo = models.ForeignKey(
        ImpostoTipo, on_delete=models.CASCADE, related_name='receita_imposto_set')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = ImpostoQuerySet.as_manager()

    class Meta:
        db_table = 'receita_imposto'
        verbose_name = 'Receita Imposto'
        verbose_name_plural = 'Receita Impostos'
        unique_together = ('loja', 'tipo')
