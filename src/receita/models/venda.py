from django.db import models

from cadastros.models import Produto, Vendedor


class Venda(models.Model):
    data = models.DateField()
    nfe = models.CharField(max_length=10)
    valor = models.DecimalField(max_digits=14, decimal_places=2)
    produto = models.ForeignKey(
        Produto, on_delete=models.CASCADE, related_name='receita_venda_set')
    vendedor = models.ForeignKey(
        Vendedor, on_delete=models.CASCADE, related_name='receita_venda_set')
    quantidade = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'receita_venda'
        verbose_name = 'Receita Venda'
        verbose_name_plural = 'Receita Vendas'
