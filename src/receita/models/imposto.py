from django.db import models

from cadastros.models.loja import Loja

from .imposto_tipo import ImpostoTipo


class Imposto(models.Model):
    percent = models.DecimalField(max_digits=5, decimal_places=2)
    loja = models.ForeignKey(
        Loja, on_delete=models.CASCADE, related_name='receita_imposto_set')
    tipo = models.ForeignKey(
        ImpostoTipo, on_delete=models.CASCADE, related_name='receita_imposto_set')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'receita_imposto'
        verbose_name = 'Receita Imposto'
        verbose_name_plural = 'Receita Impostos'
        unique_together = ('loja', 'tipo')
