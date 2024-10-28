import polars as pl
from celery import shared_task
from django.db import transaction
from django.db.models import QuerySet, Sum
from django.utils import timezone
from django.utils.functional import cached_property

from app.utils.pipiline import Pipeline

from ..models import Consolidacao, Imposto, Tipo, Venda


class LoadConsolidacao(Pipeline):
    """Extrai, transforma e carrega os dados de Receita Consolidados."""

    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.data_range = kwargs.get("data_range")
        self.vendedor_list = kwargs.get("vendedor_list")
        self.produto_list = kwargs.get("produto_list")
        self.loja_list = kwargs.get("loja_list")
        self.equipe_venda_list = kwargs.get("equipe_venda_list")

    def get_imposto_queryset(self) -> QuerySet:
        """Retorna o queryset de [Imposto]"""
        return Imposto.objects

    def get_tipo_queryset(self) -> QuerySet:
        """Retorna o queryset de [Tipo]"""
        return Tipo.objects.all()

    def get_venda_queryset(self) -> QuerySet:
        """Retorna o queryset de [Venda]"""
        return Venda.objects.filter(
            **self._filtro
        ).annotate_with_receita_bruta()

    @cached_property
    def _filtro(self) -> dict:
        filtro = {}
        if not None in self.data_range:
            filtro["data__range"] = self.data_range
        if self.vendedor_list:
            filtro["vendedor__in"] = self.vendedor_list
        if self.loja_list:
            filtro["vendedor__equipe_venda__loja__in"] = self.loja_list
        if self.equipe_venda_list:
            filtro["vendedor__equipe_venda__in"] = self.equipe_venda_list
        if self.produto_list:
            filtro["produto__in"] = self.produto_list
        return filtro

    def run(self) -> dict:
        start_polars_transform = timezone.now()
        self.extract_transform_dataset()
        finish_polars_transform = timezone.now()
        self.log["duration_transform"] = (
            finish_polars_transform - start_polars_transform
        ).total_seconds()
        self.load()
        return self.log

    def extract_transform_dataset(self) -> None:
        self.dataset = (
            self._venda_dataset.join(
                self._imposto_dataset, how="left", on=["loja_id"]
            )
            .with_columns(
                (
                    pl.col("valor_receita_bruta")
                    * (pl.col("percent_imposto") / 100)
                ).alias("valor_impostos")
            )
            .with_columns(
                (
                    (pl.col("valor_receita_bruta") - pl.col("valor_impostos"))
                    * (pl.col("percent_comissao") / 100)
                ).alias("valor_comissao")
            )
            .with_columns(
                (
                    pl.col("valor_receita_bruta")
                    - pl.col("valor_comissao")
                    - pl.col("valor_impostos")
                    - pl.col("valor_custo")
                ).alias("valor_receita_liquida")
            )
            .pipe(self._reshape_data)
            .with_columns(
                pl.col("receita_tipo")
                .replace(
                    {
                        f"valor_{obj.codigo}": obj.id
                        for obj in self.get_tipo_queryset()
                    },
                    default=None,
                )
                .alias("tipo_id")
            )
            .group_by(
                ["data", "produto_id", "vendedor_id", "tipo_id", "cliente_id"]
            )
            .agg(pl.col("valor").sum().alias("valor"))
        )

    @property
    def _venda_dataset(self) -> pl.DataFrame:
        """Retorna um dataset com os dados de [Venda]"""
        schema = {
            "data": {"rename": "data", "type": pl.Date},
            "cliente_id": {"rename": "cliente_id", "type": pl.Int64},
            "produto_id": {"rename": "produto_id", "type": pl.Int64},
            "vendedor_id": {"rename": "vendedor_id", "type": pl.Int64},
            "vendedor__equipe_venda__loja_id": {
                "rename": "loja_id",
                "type": pl.Int64,
            },
            "valor_receita_bruta": {
                "rename": "valor_receita_bruta",
                "type": pl.Float64,
            },
            "vendedor__equipe_venda__percent_comissao": {
                "rename": "percent_comissao",
                "type": pl.Float64,
            },
        }
        qs = (
            self.get_venda_queryset()
            .values(*schema.keys())
            .annotate(valor_custo=Sum("produto__custo"))
        )
        return pl.DataFrame(
            data=list(qs),
            schema=dict(
                **{k: v.get("type") for k, v in schema.items()},
                valor_custo=pl.Float64,
            ),
        ).rename({k: v["rename"] for k, v in schema.items()})

    @property
    def _imposto_dataset(self) -> pl.DataFrame:
        """Retorna um dataset com os dados de [Imposto]"""
        qs = (
            self.get_imposto_queryset()
            .values("loja_id")
            .annotate(percent_imposto=Sum("percent"))
        )
        return pl.DataFrame(
            data=list(qs),
            schema=dict(loja_id=pl.Int64, percent_imposto=pl.Float64),
        )

    def _reshape_data(self, df: pl.DataFrame) -> pl.DataFrame:
        """Transforma todas as colunas de valores em duas, uma de tipo e outra de valor."""
        return df.melt(
            id_vars=[
                "data",
                "cliente_id",
                "produto_id",
                "vendedor_id",
                "loja_id",
            ],
            value_vars=[col for col in df.columns if col.startswith("valor_")],
            value_name="valor",
            variable_name="receita_tipo",
        )

    @transaction.atomic
    def load(self) -> None:
        self._delete()
        self._save()

    def _delete(self):
        n_deleted, __ = Consolidacao.objects.filter(**self._filtro).delete()
        self.log["n_deleted"] = n_deleted

    def _save(self):
        if self.dataset.is_empty():
            return

        objs = [Consolidacao(**vals) for vals in self.dataset.to_dicts()]
        bulk = Consolidacao.objects.bulk_create(objs=objs, batch_size=1000)
        self.log["n_inserted"] = len(bulk)


@shared_task(
    name="receita.load_consolidacao",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 3},
)
def load_consolidacao_async(self, filtros: dict) -> dict:
    with LoadConsolidacao(**filtros) as task:
        log = task.run()
    return log
