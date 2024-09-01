import random

from django.core.management.base import BaseCommand
from faker import Faker

from cadastros.models import Cliente

fake = Faker('pt_BR')

ESTADOS_CIDADES = {
    'SP': ['São Paulo', 'Campinas', 'Santos'],
    'RJ': ['Rio de Janeiro', 'Niterói', 'Petrópolis'],
    'MG': ['Belo Horizonte', 'Uberlândia', 'Juiz de Fora'],
    'PR': ['Curitiba', 'Londrina', 'Maringá'],
    'RS': ['Porto Alegre', 'Caxias do Sul', 'Pelotas'],
    'SC': ['Florianópolis', 'Joinville', 'Blumenau'],
    'BA': ['Salvador', 'Feira de Santana', 'Vitória da Conquista'],
    'DF': ['Brasília'],
    'CE': ['Fortaleza', 'Caucaia', 'Juazeiro do Norte'],
    'PE': ['Recife', 'Olinda', 'Jaboatão dos Guararapes'],
    'AM': ['Manaus', 'Parintins', 'Itacoatiara'],
    'PA': ['Belém', 'Santarém', 'Ananindeua'],
    'GO': ['Goiânia', 'Anápolis', 'Aparecida de Goiânia'],
    'MA': ['São Luís', 'Imperatriz', 'Timon'],
    'AL': ['Maceió', 'Arapiraca', 'Rio Largo'],
    'RN': ['Natal', 'Mossoró', 'Parnamirim'],
    'PI': ['Teresina', 'Parnaíba', 'Picos'],
    'PB': ['João Pessoa', 'Campina Grande', 'Patos']
}


class Command(BaseCommand):
    help = 'Cria registros aleatórios de Cliente'

    def handle(self, *args, **kwargs):
        created_count = 0
        attempts = 0
        max_attempts = 5000
        qtd_registros = 1800

        while created_count < qtd_registros and attempts < max_attempts:
            estado = random.choice(list(ESTADOS_CIDADES.keys()))
            cliente_data = {
                'nome': fake.name(),
                'cpf': fake.cpf(),
                'bairro': fake.bairro(),
                'cep': fake.postcode(),
                'cidade': random.choice(ESTADOS_CIDADES[estado]),
                'email': fake.email(),
                'rua': fake.street_name(),
                'uf': estado,
            }

            if not Cliente.objects.filter(cpf=cliente_data['cpf']).exists():
                Cliente.objects.create(**cliente_data)
                created_count += 1

            attempts += 1

        self.stdout.write(self.style.SUCCESS(
            f'{created_count} clientes aleatórios foram criados com sucesso. Foram feitas {attempts} tentativas'))
        if created_count < qtd_registros:
            self.stdout.write(self.style.WARNING(
                f'Atingido o limite de tentativas ({attempts}), foram criados {created_count} clientes.'))
