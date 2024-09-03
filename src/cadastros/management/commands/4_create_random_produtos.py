import random

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from cadastros.models import Fornecedor, GrupoProduto, Produto


class Command(BaseCommand):
    help = 'Create initial product records'

    def handle(self, *args, **kwargs):
        grupos_de_produtos = {
            'Bicicletas para Adultos': ['Bicicleta Aro 29', 'Mountain Bike', 'Speed Bike', 'Bicicleta Elétrica', 'Bicicleta de Estrada'],
            'Bicicletas para Crianças': ['Bicicleta Aro 13', 'Bicicleta Aro 16', 'Bicicleta Aro 18', 'Bicicleta com Rodinhas', 'Bicicleta Balance'],
            'Capacetes': ['Capacete de Estrada', 'Capacete de Montanha', 'Capacete Infantil', 'Capacete de Speed', 'Capacete Urbano'],
            'Luzes e Refletores': ['Luz Dianteira', 'Luz Traseira', 'Refletores de Roda', 'Refletor de Guidão', 'Kit de Iluminação'],
            'Pneus e Câmaras de Ar': ['Pneu Aro 29', 'Pneu Aro 26', 'Câmara de Ar Aro 20', 'Câmara de Ar Aro 16', 'Pneu de Montanha'],
            'Selins e Rodas': ['Selim Confortável', 'Selim de Competição', 'Roda Dianteira Aro 29', 'Roda Traseira Aro 29', 'Roda de Estrada'],
            'Ferramentas e Manutenção': ['Bomba de Ar', 'Kit de Reparo de Pneus', 'Lubrificante de Corrente', 'Jogo de Chaves Allen', 'Suporte de Manutenção'],
            'Roupas e Acessórios': ['Camiseta de Ciclista', 'Bermuda de Ciclista', 'Jaqueta corta-vento', 'Luvas de Ciclista', 'Meias de Compressão'],
            'Suportes e Grades': ['Suporte para Carro', 'Suporte de Parede', 'Grade de Capacete', 'Grade para Bagageiro', 'Suporte para Garrafa'],
            'Cadeados e Correntes': ['Cadeado com Chave', 'Cadeado com Segredo', 'Corrente de Segurança', 'Cadeado U-Lock', 'Cadeado Flexível']
        }

        custo_ranges = {
            'Bicicletas para Adultos': (750.00, 15000.00),
            'Bicicletas para Crianças': (500.00, 2000.00),
            'Capacetes': (100.00, 500.00),
            'Luzes e Refletores': (20.00, 150.00),
            'Pneus e Câmaras de Ar': (30.00, 200.00),
            'Selins e Rodas': (50.00, 500.00),
            'Ferramentas e Manutenção': (15.00, 300.00),
            'Roupas e Acessórios': (30.00, 250.00),
            'Suportes e Grades': (30.00, 400.00),
            'Cadeados e Correntes': (20.00, 200.00)
        }

        todos_fornecedores = list(Fornecedor.objects.all())

        for grupo_nome, produtos in grupos_de_produtos.items():
            try:
                grupo = GrupoProduto.objects.get(nome=grupo_nome)
            except GrupoProduto.DoesNotExist:
                self.stderr.write(self.style.ERROR(
                    f'Grupo {grupo_nome} não encontrado!'))
                continue

            for nome_produto in produtos:
                fornecedor_selecionados = random.sample(todos_fornecedores, 3)
                min_custo, max_custo = custo_ranges[grupo_nome]

                for ix in range(3):
                    codigo = f'{grupo_nome[:3].upper()}{nome_produto[:3].upper()}{random.randint(100, 999):03d}'
                    sku = f'{nome_produto[:3].upper()}{ix:02d}SKU'
                    try:
                        produto = Produto.objects.create(
                            nome=nome_produto,
                            codigo=codigo,
                            custo=random.uniform(min_custo, max_custo),
                            grupo_produto=grupo,
                            fornecedor=fornecedor_selecionados[ix],
                            sku=sku
                        )
                        self.stdout.write(self.style.SUCCESS(
                            f'Produto {produto.nome} criado com sucesso.'))
                    except IntegrityError:
                        self.stderr.write(self.style.ERROR(
                            f'Código {codigo} já existe! Produto {nome_produto} com fornecedor {fornecedor_selecionados[ix].nome} não pôde ser criado.'))

        self.stdout.write(self.style.SUCCESS('Complete!'))
