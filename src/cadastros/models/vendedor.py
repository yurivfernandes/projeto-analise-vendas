from django.db import models
from django.db.models import F, Value
from django.db.models.functions import Concat

from .equipe_venda import EquipeVenda


class VendedorQuerySet(models.QuerySet):
    """Classe que customiza o QuerySet da model principal"""

    def annotate_with_equipe_venda_related(self) -> models.QuerySet:
        """Retorna um queryset com dados relacionados ao Vendedor"""
        return (
            self
            .select_related('equipe_venda')
            .annotate(
                equipe_venda__label=Concat(
                    F('equipe_venda__codigo'),
                    Value(' | '),
                    F('equipe_venda__nome')),
                loja__label=Concat(
                    F('equipe_venda__loja__codigo'),
                    Value(' | '),
                    F('equipe_venda__loja__nome'))
            )
        )


class Vendedor(models.Model):
    nome = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, unique=True)
    equipe_venda = models.ForeignKey(
        EquipeVenda, on_delete=models.CASCADE, related_name='cadastro_vendedor_set')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = VendedorQuerySet.as_manager()

    class Meta:
        db_table = 'cadastro_vendedor'
        verbose_name = 'Cadastro Vendedor'
        verbose_name_plural = 'Cadastro Vendedores'
        unique_together = ('nome', 'codigo')
