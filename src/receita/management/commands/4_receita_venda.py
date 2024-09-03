import random
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.timezone import make_aware

from cadastros.models import Produto, Vendedor
from receita.models import Venda


class Command(BaseCommand):
    help = 'Populate the Venda model with realistic data.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Inicializando o processo'))
        start_date = datetime(2010, 1, 1)
        end_date = datetime.now()
        holidays = [(12, 25), (1, 1)]
        nfe_counter = 1
        stores = {
            "São Paulo": 380000,
            "Rio de Janeiro": 300000,
            "Belo Horizonte": 280000,
            "Curitiba": 270000,
            "Porto Alegre": 220000,
            "Brasília": 220000,
            "Salvador": 200000,
            "Fortaleza": 200000,
            "Recife": 200000,
            "Belém": 180000,
            "Goiânia": 180000,
            "Manaus": 180000,
            "Florianópolis": 180000,
            "São Luís": 180000,
            "Maceió": 180000,
            "Vitória": 180000,
            "Natal": 180000,
            "Teresina": 180000,
            "João Pessoa": 180000,
            "Aracaju": 180000,
            "Campo Grande": 180000,
            "Cuiabá": 180000,
            "Porto Velho": 180000,
            "Macapá": 180000,
            "Palmas": 180000,
            "Boa Vista": 180000,
            "Rio Branco": 180000
        }
        products = Produto.objects.all()
        product_weights = {
            'Bicicletas para Adultos': 0.30,
            'Bicicletas para Crianças': 0.25,
            'Ferramentas e Manutenção': 0.20,
            'Capacetes': 0.05,
            'Luzes e Refletores': 0.05,
            'Pneus e Câmaras de Ar': 0.05,
            'Selins e Rodas': 0.03,
            'Roupas e Acessórios': 0.03,
            'Suportes e Grades': 0.02,
            'Cadeados e Correntes': 0.02
        }
        product_group_weights = {
            product.grupo_produto.nome: product_weights[product.grupo_produto.nome] for product in products}
        products_list = list(products)
        products_weights = [
            product_group_weights[product.grupo_produto.nome] for product in products]
        vendors = list(Vendedor.objects.all())

        with transaction.atomic():
            current_date = start_date
            while current_date <= end_date:
                if not (current_date.month, current_date.day) in holidays:
                    for store, avg_sales in stores.items():
                        if current_date.month == 12:
                            avg_sales = avg_sales * 1.5
                        daily_sales_target = avg_sales / 30
                        total_daily_sales = 0

                        while total_daily_sales < daily_sales_target:
                            num_products = random.randint(1, 3)
                            selected_products = random.choices(
                                products_list, weights=products_weights, k=num_products)
                            vendor = random.choice(vendors)
                            venda_nfe = str(nfe_counter).zfill(10)

                            for product in selected_products:
                                preco_venda = float(
                                    product.custo) + (float(product.custo) * float(random.uniform(0.3, 0.55)))
                                quantidade = random.randint(1, 3)
                                venda_total = preco_venda * quantidade

                                Venda.objects.create(
                                    data=current_date,
                                    nfe=venda_nfe,
                                    valor=preco_venda,
                                    produto=product,
                                    vendedor=vendor,
                                    quantidade=quantidade)

                                total_daily_sales += venda_total

                            nfe_counter += 1
                current_date += timedelta(days=1)

        self.stdout.write(self.style.SUCCESS('Data population complete.'))
