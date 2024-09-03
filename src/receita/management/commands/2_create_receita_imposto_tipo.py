from django.core.management.base import BaseCommand

from receita.models.imposto_tipo import ImpostoTipo


class Command(BaseCommand):
    help = 'Preenche a tabela ImpostoTipo com os tipos de imposto iniciais'

    def handle(self, *args, **kwargs):
        tipos_imposto = ['ICMS', 'ISS', 'IPI', 'PIS', 'Cofins']
        for tipo in tipos_imposto:
            if not ImpostoTipo.objects.filter(nome=tipo).exists():
                ImpostoTipo.objects.create(nome=tipo)
                self.stdout.write(self.style.SUCCESS(
                    f'Tipo de imposto "{tipo}" adicionado com sucesso.'))
            else:
                self.stdout.write(self.style.WARNING(
                    f'Tipo de imposto "{tipo}" já existe.'))
