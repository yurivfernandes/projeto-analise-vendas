# cadastros/management/commands/inserir_equipes.py

from django.core.management.base import BaseCommand
from django.db import transaction

from cadastros.models import EquipeVenda, Loja


class Command(BaseCommand):
    help = 'Insere 5 equipes de vendas para cada loja'

    def handle(self, *args, **options):
        # Define the teams and their commission percentages
        teams = [
            {'name': 'Equipe Starter', 'percent_comissao': 5.00},
            {'name': 'Equipe Avançada', 'percent_comissao': 7.50},
            {'name': 'Equipe Expert', 'percent_comissao': 10.00},
            {'name': 'Equipe Master', 'percent_comissao': 12.50},
            {'name': 'Equipe Elite', 'percent_comissao': 15.00},
        ]

        try:
            with transaction.atomic():
                lojas = Loja.objects.all()
                for loja in lojas:
                    for idx, team in enumerate(teams, start=1):
                        codigo = f'L{loja.id}E{idx:02d}'
                        EquipeVenda.objects.create(
                            codigo=codigo,
                            loja=loja,
                            nome=team['name'],
                            percent_comissao=team['percent_comissao']
                        )
                self.stdout.write(self.style.SUCCESS(
                    'Equipes de vendas foram inseridas com sucesso.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ocorreu um erro: {str(e)}'))
