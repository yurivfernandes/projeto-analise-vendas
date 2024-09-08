from django.db import models


class Tipo(models.Model):
    nome = models.CharField(max_length=255, unique=True)
    codigo = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'receita_tipo'
        verbose_name = 'Receita Tipo'
        verbose_name_plural = 'Receita Tipos'
