import random
import string

from django.core.management.base import BaseCommand

from cadastros.models.grupo_produto import GrupoProduto


class Command(BaseCommand):
    help = 'Populate the GrupoProduto model with initial data'

    def handle(self, *args, **kwargs):
        produto_grupos = [
            'Bicicletas para Adultos',
            'Bicicletas para Crianças',
            'Capacetes',
            'Luzes e Refletores',
            'Pneus e Câmaras de Ar',
            'Selins e Rodas',
            'Ferramentas e Manutenção',
            'Roupas e Acessórios',
            'Suportes e Grades',
            'Cadeados e Correntes'
        ]

        def generate_unique_code():
            # Generate a random string of 10 characters
            return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

        # Clear existing entries
        GrupoProduto.objects.all().delete()

        for nome in produto_grupos:
            codigo = generate_unique_code()
            while GrupoProduto.objects.filter(codigo=codigo).exists():
                codigo = generate_unique_code()

            GrupoProduto.objects.create(nome=nome, codigo=codigo)
            self.stdout.write(self.style.SUCCESS(
                f'GrupoProduto "{nome}" ({codigo}) created successfully!'))
