from django.core.management.base import BaseCommand

from cadastros.models.loja import Loja
from receita.models.imposto import Imposto
from receita.models.imposto_tipo import ImpostoTipo


class Command(BaseCommand):
    help = 'Cria registros de impostos com valores predefinidos'

    ICMS_POR_ESTADO = {
        'AC': 17.00,
        'AL': 18.00,
        'AP': 18.00,
        'AM': 18.00,
        'BA': 17.00,
        'CE': 18.00,
        'DF': 18.00,
        'ES': 17.00,
        'GO': 17.00,
        'MA': 18.00,
        'MT': 17.00,
        'MS': 17.00,
        'MG': 18.00,
        'PA': 17.00,
        'PB': 18.00,
        'PR': 18.00,
        'PE': 18.00,
        'PI': 18.00,
        'RJ': 19.00,
        'RN': 18.00,
        'RS': 18.00,
        'RO': 17.50,
        'RR': 17.00,
        'SC': 17.00,
        'SP': 18.00,
        'SE': 18.00,
        'TO': 18.00,
    }

    ISS_POR_CIDADE = {
        'Rio Branco': 2.00,
        'Maceió': 2.50,
        'Macapá': 3.00,
        'Manaus': 2.00,
        'Salvador': 3.00,
        'Fortaleza': 2.00,
        'Brasília': 2.50,
        'Vitória': 2.00,
        'Goiânia': 2.50,
        'São Luís': 3.00,
        'Cuiabá': 2.00,
        'Campo Grande': 2.50,
        'Belo Horizonte': 2.50,
        'Belém': 2.00,
        'João Pessoa': 2.50,
        'Curitiba': 2.75,
        'Recife': 2.50,
        'Teresina': 2.50,
        'Rio de Janeiro': 3.00,
        'Natal': 3.00,
        'Porto Alegre': 2.50,
        'Porto Velho': 2.00,
        'Boa Vista': 3.00,
        'Florianópolis': 2.00,
        'São Paulo': 2.00,
        'Aracaju': 2.50,
        'Palmas': 3.00,
    }

    def handle(self, *args, **kwargs):
        lojas = Loja.objects.all()

        impostos_tipos = {
            'ICMS': {},
            'ISS': {},
        }

        for nome, dados in impostos_tipos.items():
            tipo, created = ImpostoTipo.objects.get_or_create(nome=nome)
            for loja in lojas:
                percent = dados.get('default_percent', 0)

                if nome == 'ICMS':
                    percent = self.ICMS_POR_ESTADO.get(loja.uf)
                elif nome == 'ISS':
                    percent = self.ISS_POR_CIDADE.get(loja.cidade)

                Imposto.objects.get_or_create(
                    loja=loja,
                    tipo=tipo,
                    defaults={'percent': percent}
                )

        self.stdout.write(self.style.SUCCESS('Impostos criados com sucesso!'))
