from django.core.management.base import BaseCommand
from faker import Faker

from cadastros.models import Loja


class Command(BaseCommand):
    help = 'Popula a tabela Loja com dados aleatórios para as capitais brasileiras.'

    def handle(self, *args, **kwargs):
        fake = Faker('pt_BR')
        capitais = [
            "Rio de Janeiro", "São Paulo", "Belo Horizonte", "Brasília", "Salvador",
            "Fortaleza", "Curitiba", "Recife", "Porto Alegre", "Belém",
            "Goiânia", "Manaus", "Florianópolis", "São Luís", "Maceió",
            "Vitória", "Natal", "Teresina", "João Pessoa", "Aracaju",
            "Campo Grande", "Cuiabá", "Porto Velho", "Macapá", "Palmas",
            "Boa Vista", "Rio Branco"
        ]

        for cidade in capitais:
            if Loja.objects.filter(cidade=cidade).exists():
                self.stdout.write(self.style.WARNING(
                    f'Uma loja já existe em {cidade}, pulando...'))
                continue

            nome_loja = f'Shopping {cidade}'
            uf = fake.estado_sigla()
            loja = Loja.objects.create(
                nome=nome_loja,
                codigo=fake.bothify(
                    text='??-#####', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
                bairro=fake.bairro(),
                cep=fake.postcode(),
                cidade=cidade,
                cnpj=fake.cnpj(),
                email=fake.email(),
                rua=fake.street_name(),
                telefone=fake.phone_number(),
                uf=uf
            )
            loja.save()

        self.stdout.write(self.style.SUCCESS(
            'Tabela de lojas preenchida com sucesso!'))
