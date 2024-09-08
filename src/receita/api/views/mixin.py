
from datetime import datetime

import polars as pl
from django.db import models
from django.db.models import QuerySet
from pandas import date_range
from rest_framework.request import Request
from rest_framework.response import Response

from ...models import Consolidacao


class Mixin:

    def get(self, request: Request, *args, **kwargs) -> Response:
        self.data_range = (
            request.GET.get('data_inicio'),
            request.GET.get('data_fim'))
        self._set_date_maps()
        return Response(self.main())

    def get_consolidacao_queryset(self) -> QuerySet:
        return Consolidacao.objects.filter(data__range=self.data_range)

    def _set_date_maps(self) -> None:
        """Define o mapeamento entre datas em formato datetime.date e a string para consumo do front"""
        dt_list = [datetime.strptime(dt, '%Y-%m-%d') for dt in self.data_range]

        self.date_map = {
            d.date().isoformat(): f"{d.strftime('%Y')}-{d.strftime('%m')}"
            for d in
            date_range(
                start=min(dt_list).replace(day=1),
                end=max(dt_list).replace(day=1),
                freq="MS")
        }
        self.date_columns = [f'{dt}' for dt in self.date_map.values()]

    def main(self) -> list:
        """Implementar o método main retornando um DataFrame"""
        raise NotImplementedError("Subclass must implement this method")

    def _get_dataset(self, query_set: models.QuerySet, schema: dict) -> pl.DataFrame:
        """Retorna os dados do queryset em formato de dataframe"""
        return (
            pl.DataFrame(
                data=list(query_set),
                schema=dict(
                    **{k: v.get('type') for k, v in schema.items()}
                )
            )
            .rename({k: v['rename'] for k, v in schema.items()}))

    def _extract_and_transform_dataset(self, df: pl.DataFrame) -> None:
        """Implementar o método que carrega e transforma o dataset principal para o main"""
        self.dataset = (
            df
            .with_columns(
                pl.col('data')
                .dt
                .truncate("1mo")
                .alias('data')
            )
            .pipe(self._replace_with_date_map)
            .sort(['data'])
            .pipe(self._pivot_dataset)
            .pipe(self._ensure_date_cols)
            .fill_null(0)
            .with_columns(
                pl.arange(0, pl.count())
                .cast(pl.Utf8)
                .str.zfill(4)
                .alias("key")
            )
        )

    def _replace_with_date_map(self, df: pl.DataFrame) -> pl.DataFrame:
        return df.with_columns(data=pl.col('data').replace(self.date_map, default=None)).drop_nulls(subset='data')

    def _pivot_dataset(self, df: pl.DataFrame) -> pl.DataFrame:
        """Efetua o pivot dos dados transformando as colunas de valor em data e valor."""
        idx_columns = [
            c for c in df.columns
            if c not in ['valor', 'data']]
        return (
            df
            .with_row_count("index")
            .pivot(
                values=['valor'],
                index=idx_columns,
                columns='data',
                aggregate_function='first'))

    def _ensure_date_cols(self, df: pl.DataFrame) -> pl.DataFrame:
        cols = [c for c in self.date_columns if c not in df.columns]
        return df.with_columns(*[pl.lit(0.0).alias(c) for c in cols])
