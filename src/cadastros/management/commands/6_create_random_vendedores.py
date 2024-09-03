import random

from django.core.management.base import BaseCommand
from faker import Faker

from cadastros.models import EquipeVenda, Loja, Vendedor


class Command(BaseCommand):
    help = 'Populates the Vendedor model with sample data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        team_constraints = {
            'Equipe Elite': 1,
            'Equipe Master': 2,
            'Equipe Expert': 3,
            'Equipe Avançada': (2, 6),  # range for simulation of average
            'Equipe Starter': (5, 10)
        }

        lojas = Loja.objects.all()

        for loja in lojas:
            for equipe_nome, constraint in team_constraints.items():
                try:
                    equipe_venda = EquipeVenda.objects.get(
                        nome=equipe_nome, loja=loja)
                except EquipeVenda.DoesNotExist:
                    self.stderr.write(self.style.ERROR(
                        f"EquipeVenda '{equipe_nome}' does not exist for Loja '{loja}'"))
                    continue

                num_vendedores = constraint
                if isinstance(constraint, tuple):
                    num_vendedores = random.randint(*constraint)

                for _ in range(num_vendedores):
                    nome = fake.name()
                    codigo = ''.join(fake.random_letters(length=10))

                    try:
                        Vendedor.objects.create(
                            nome=nome,
                            codigo=codigo,
                            equipe_venda=equipe_venda
                        )
                    except Exception as e:
                        self.stderr.write(self.style.ERROR(
                            f"Error creating Vendedor: {e}"))

        self.stdout.write(self.style.SUCCESS(
            'Successfully populated Vendedor model'))
