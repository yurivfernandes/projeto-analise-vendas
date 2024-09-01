from django.db import models


class Fornecedor(models.Model):
    codigo = models.CharField(max_length=15)
    nome = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cadastro_fornecedor'
        verbose_name = 'Cadastros de Fornecedor'
        verbose_name_plural = 'Cadastros de Fornecedores'
        unique_together = ('nome', 'codigo')
