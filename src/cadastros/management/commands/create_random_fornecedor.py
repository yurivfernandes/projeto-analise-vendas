from django.core.management.base import BaseCommand
from faker import Faker

from cadastros.models import Fornecedor

fake = Faker('pt_BR')


class Command(BaseCommand):
    help = 'Cria registros aleatórios de Fornecedor'

    def handle(self, *args, **kwargs):
        created_count = 0
        attempts = 0
        max_attempts = 1000
        qtd_registros = 350

        while created_count < qtd_registros and attempts < max_attempts:
            nome = fake.company()
            cnpj = fake.cnpj()

            if not Fornecedor.objects.filter(cnpj=cnpj).exists():
                Fornecedor.objects.create(
                    cnpj=cnpj,
                    nome=nome,
                )
                created_count += 1

            attempts += 1

        self.stdout.write(self.style.SUCCESS(
            f'{created_count} fornecedores aleatórios foram criados com sucesso. Foram feitas {attempts} tentativas!'))
        if created_count < qtd_registros:
            self.stdout.write(self.style.WARNING(
                f'Atingido o limite de tentativas ({attempts}), foram criados {created_count} fornecedores.'))
