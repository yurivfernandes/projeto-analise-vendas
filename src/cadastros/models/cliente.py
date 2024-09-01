from django.db import models


class Cliente(models.Model):
    bairro = models.CharField(max_length=255)
    cep = models.CharField(max_length=8)
    cidade = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True)
    email = models.CharField(max_length=300)
    nome = models.CharField(max_length=255)
    rua = models.CharField(max_length=255)
    uf = models.CharField(max_length=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cadastro_cliente'
        verbose_name = 'Cadastros Cliente'
        verbose_name_plural = 'Cadastros Clientes'
