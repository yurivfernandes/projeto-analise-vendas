from django.db import models
from django.db.models import F, Value
from django.db.models.functions import Concat

from .loja import Loja


class LojaQuerySet(models.QuerySet):
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


class EquipeVenda(models.Model):
    codigo = models.CharField(max_length=10)
    loja = models.ForeignKey(
        Loja, on_delete=models.CASCADE, related_name='cadastros_equipe_venda_set')
    nome = models.CharField(max_length=25)
    percent_comissao = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = LojaQuerySet.as_manager()

    class Meta:
        db_table = 'cadastro_equipe_venda'
        verbose_name = 'Cadastro Equipe de Venda'
        verbose_name_plural = 'Cadastros Equipes de Vendas'
        unique_together = ('nome', 'codigo', 'loja')
