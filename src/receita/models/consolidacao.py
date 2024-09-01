from django.db import models

from cadastros.models import Produto, Vendedor

from .tipo import Tipo


class Consolidacao(models.Model):
    data = models.DateField()
    valor = models.DecimalField(max_digits=14, decimal_places=2)
    tipo = models.ForeignKey(
        Tipo, on_delete=models.CASCADE, related_name='receita_consolidacao_set')
    vendedor = models.ForeignKey(
        Vendedor, on_delete=models.CASCADE, related_name='receita_consolidacao_set')
    produto = models.ForeignKey(
        Produto, on_delete=models.CASCADE, related_name='receita_consolidacao_set')
    quantidade = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'receita_consolidacao'
        verbose_name = 'Receita Consolidação'
        verbose_name_plural = 'Consolidação de Receita'
