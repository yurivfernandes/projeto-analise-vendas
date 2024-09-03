from django.db import models

from .equipe_venda import EquipeVenda


class Vendedor(models.Model):
    nome = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10,unique=True)
    equipe_venda = models.ForeignKey(
        EquipeVenda, on_delete=models.CASCADE, related_name='cadastro_vendedor_set')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cadastro_vendedor'
        verbose_name = 'Cadastro Vendedor'
        verbose_name_plural = 'Cadastro Vendedores'
        unique_together = ('nome', 'codigo')
