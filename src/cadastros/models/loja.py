from django.db import models


class Loja(models.Model):
    nome = models.CharField(max_length=255, unique=True)
    codigo = models.CharField(max_length=15, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'cadastro_loja'
        verbose_name = 'Cadastros de Loja'
        verbose_name_plural = 'Cadastros de Lojas'
