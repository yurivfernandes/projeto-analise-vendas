from django.db import models

from .loja import Loja


class EquipeVenda(models.Model):
    codigo = models.CharField(max_length=10)
    loja = models.ForeignKey(
        Loja, on_delete=models.CASCADE, related_name='cadastros_equipe_venda_set')
    nome = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cadastro_equipe_venda'
        verbose_name = 'Cadastro Equipe de Venda'
        verbose_name_plural = 'Cadastros Equipes de Vendas'
        unique_together = ('nome', 'codigo', 'loja')
