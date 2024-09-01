from django.db import models

from .fornecedor import Fornecedor
from .grupo_produto import GrupoProduto


class Produto(models.Model):
    nome = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10)
    custo = models.DecimalField(max_digits=14, decimal_places=2)
    grupo_produto = models.ForeignKey(
        GrupoProduto, on_delete=models.CASCADE, related_name='cadastros_produto_set')
    fornecedor = models.ForeignKey(
        Fornecedor, on_delete=models.CASCADE, related_name='cadastros_produto_set')
    sku = models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cadastro_produto'
        verbose_name = 'Cadastros de Produto'
        verbose_name_plural = 'Cadastros de Produtos'
        unique_together = ('nome', 'codigo')
