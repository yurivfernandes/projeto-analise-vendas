import polars as pl
from rest_framework.generics import ListAPIView

from .mixin import Mixin


class ConsolidacaoProdutoAnaliseMensal(Mixin, ListAPIView):
    """Retorna o relatório em forma de painel para consumo no front conforme os dados de indicadores"""

    def main(self) -> list:
        schema = {
            'produto__nome': {'rename': 'produto', 'type': pl.String},
            'produto__codigo': {'rename': 'produto_codigo', 'type': pl.String},
            'data': {'rename': 'data', 'type': pl.Date},
            'valor': {'rename': 'valor', 'type': pl.Float64}}
        qs = (
            self.get_consolidacao_queryset()
            .values(*schema))
        self._extract_and_transform_dataset(
            df=self._get_dataset(query_set=qs, schema=schema))
        return self.dataset.sort('key').to_dicts()