from django.core.validators import RegexValidator
from django.db import models


class Loja(models.Model):
    telefone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="O número de telefone deve estar no formato '+999999999'. Até 15 dígitos permitidos."
    )
    nome = models.CharField(max_length=255, unique=True)
    codigo = models.CharField(max_length=15, unique=True)
    bairro = models.CharField(max_length=255)
    cep = models.CharField(max_length=8)
    cidade = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=15, unique=True)
    email = models.CharField(max_length=300)
    rua = models.CharField(max_length=255)
    telefone = models.CharField(
        validators=[telefone_regex], max_length=17, blank=True)
    uf = models.CharField(max_length=2)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'cadastro_loja'
        verbose_name = 'Cadastros de Loja'
        verbose_name_plural = 'Cadastros de Lojas'
