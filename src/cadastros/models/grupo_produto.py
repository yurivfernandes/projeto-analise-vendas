from django.db import models


class GrupoProduto(models.Model):
    nome = models.CharField(max_length=25, unique=True)
    codigo = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cadastro_grupo_produto'
        verbose_name = 'Cadastros de Grupo de Produto'
        verbose_name_plural = 'Cadastros de Grupos de Produtos'
