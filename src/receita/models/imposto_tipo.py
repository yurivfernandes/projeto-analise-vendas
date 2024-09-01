from django.db import models


class ImpostoTipo(models.Model):
    nome = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'receita_imposto_tipo'
        verbose_name = 'Receita Tipo Imposto'
        verbose_name_plural = 'Receita Tipos Impostos'
