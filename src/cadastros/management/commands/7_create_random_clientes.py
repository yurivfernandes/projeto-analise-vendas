import re

from django.core.management.base import BaseCommand
from faker import Faker

from cadastros.models import Cliente


class Command(BaseCommand):
    help = "Popula a tabela Cliente com dados aleatórios brasileiros"

    def handle(self, *args, **kwargs):
        fake = Faker("pt_BR")
        clientes = []
        qtd_clientes = 250
        for _ in range(qtd_clientes):
            endereco_completo = fake.address()
            endereco_linhas = endereco_completo.split("\n")
            rua = endereco_linhas[0]
            bairro = endereco_linhas[1]
            linha_cep_cidade_uf = endereco_linhas[2]
            cep = re.findall(r"\d+", linha_cep_cidade_uf)[0]
            cidade_uf = linha_cep_cidade_uf.split(" ", 1)[1]
            cidade, uf = cidade_uf.rsplit(" / ", 1)
            cliente = Cliente(
                nome=fake.name(),
                cpf=fake.cpf(),
                email=fake.email(),
                bairro=bairro,
                cep=cep,
                cidade=cidade.strip(),
                uf=uf.strip(),
                rua=rua,
            )
            clientes.append(cliente)

        # Salva todos os clientes de uma vez
        Cliente.objects.bulk_create(clientes)
        self.stdout.write(
            self.style.SUCCESS(
                f"{qtd_clientes} clientes inseridos com sucesso!"
            )
        )
