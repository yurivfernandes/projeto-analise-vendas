from django.core.management.base import BaseCommand

from receita.models import Tipo


class Command(BaseCommand):
    help = 'Insere tipos de receita no banco de dados'

    def handle(self, *args, **options):
        tipos_de_receita = {
            'RECEITA BRUTA': 'receita_bruta',
            'RECEITA LÍQUIDA': 'receita_liquida',
            'CUSTO': 'custo',
            'IMPOSTOS': 'impostos',
            'COMISSÃO': 'comissao'
        }

        for nome, codigo in tipos_de_receita.items():
            Tipo.objects.get_or_create(nome=nome, codigo=codigo)

        self.stdout.write(self.style.SUCCESS(
            'Tipos de receita inseridos com sucesso!'))
