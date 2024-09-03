from django.core.management.base import BaseCommand

from receita.models import Tipo


class Command(BaseCommand):
    help = 'Insere tipos de receita no banco de dados'

    def handle(self, *args, **options):
        tipos_de_receita = [
            'Receita Bruta',
            'Receita Líquida',
            'Impostos',
            'Comissão'
        ]

        for tipo in tipos_de_receita:
            Tipo.objects.get_or_create(nome=tipo)

        self.stdout.write(self.style.SUCCESS(
            'Tipos de receita inseridos com sucesso!'))
