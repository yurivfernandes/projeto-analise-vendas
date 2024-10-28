import pandas as pd
from celery import shared_task
from django.db import transaction
from django.db.models import QuerySet, Sum
from django.utils import timezone
from django.utils.functional import cached_property

from app.utils.pipiline import Pipeline

from ..models import Consolidacao, Imposto, Tipo, Venda


class LoadConsolidacaoPandas(Pipeline):
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
        start_pandas_transform = timezone.now()
        self.extract_transform_dataset()
        finish_pandas_transform = timezone.now()
        self.log["duration_transform"] = (
            finish_pandas_transform - start_pandas_transform
        ).total_seconds()
        self.load()
        return self.log

    def extract_transform_dataset(self) -> None:
        self.dataset = (
            self._venda_dataset.merge(
                self._imposto_dataset, how="left", on=["loja_id"]
            )
            .assign(
                valor_impostos=lambda d_: (
                    d_["valor_receita_bruta"] * (d_["percent_imposto"] / 100)
                ).round(2),
                valor_comissao=lambda d_: (
                    (d_["valor_receita_bruta"] - d_["valor_impostos"])
                    * (d_["percent_comissao"] / 100)
                ).round(2),
                valor_receita_liquida=lambda d_: (
                    d_["valor_receita_bruta"]
                    - d_["valor_comissao"]
                    - d_["valor_impostos"]
                    - d_["valor_custo"]
                ).round(2),
            )
            .pipe(self._reshape_data)
            .assign(
                tipo_id=lambda d_: (
                    d_["receita_tipo"].map(
                        {
                            f"valor_{obj.codigo}": obj.id
                            for obj in self.get_tipo_queryset()
                        }
                    )
                )
            )
            .groupby(
                [
                    "data",
                    "produto_id",
                    "vendedor_id",
                    "cliente_id",
                    "tipo_id",
                ],
                as_index=False,
            )
            .agg({"valor": "sum"})
            .astype(
                {
                    "data": "datetime64[D]",
                    "cliente_id": "int",
                    "produto_id": "int",
                    "vendedor_id": "int",
                    "tipo_id": "int",
                    "valor": "float",
                }
            )
        )

    @property
    def _venda_dataset(self) -> pd.DataFrame:
        """Retorna um dataset com os dados de [Venda]"""
        field_map = {
            "data": "data",
            "produto_id": "produto_id",
            "vendedor_id": "vendedor_id",
            "valor_receita_bruta": "valor_receita_bruta",
            "vendedor__equipe_venda__percent_comissao": "percent_comissao",
            "vendedor__equipe_venda__loja_id": "loja_id",
            "cliente_id": "cliente_id",
        }
        qs = (
            self.get_venda_queryset()
            .values(*field_map)
            .annotate(valor_custo=Sum("produto__custo"))
        )
        return (
            pd.DataFrame(
                data=qs, columns=list(field_map.keys()) + ["valor_custo"]
            )
            .rename(columns=field_map)
            .astype(
                dtype={
                    "data": "datetime64[ns]",
                    "produto_id": "int64",
                    "vendedor_id": "int64",
                    "loja_id": "int64",
                    "valor_receita_bruta": "float64",
                    "valor_custo": "float64",
                    "percent_comissao": "float64",
                }
            )
            .round(2)
        )

    @property
    def _imposto_dataset(self) -> pd.DataFrame:
        """Retorna um dataset com os dados de [Imposto]"""
        qs = (
            self.get_imposto_queryset()
            .values("loja_id")
            .annotate(percent_imposto=Sum("percent"))
        )
        return pd.DataFrame(
            data=qs, columns=["loja_id", "percent_imposto"]
        ).astype(dtype={"loja_id": "int64", "percent_imposto": "float64"})

    def _reshape_data(self, df: pd.DataFrame) -> pd.DataFrame:
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
            var_name="receita_tipo",
            value_name="valor",
        )

    @transaction.atomic
    def load(self) -> None:
        self._delete()
        self._save()

    def _delete(self):
        n_deleted, __ = Consolidacao.objects.filter(**self._filtro).delete()
        self.log["n_deleted"] = n_deleted

    def _save(self):
        if self.dataset.empty:
            return

        objs = [
            Consolidacao(**vals) for vals in self.dataset.to_dict("records")
        ]
        bulk = Consolidacao.objects.bulk_create(objs=objs, batch_size=1000)
        self.log["n_inserted"] = len(bulk)


@shared_task(
    name="receita.load_consolidacao_pandas",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 3},
)
def load_consolidacao_pandas_async(self, filtros: dict) -> dict:
    with LoadConsolidacaoPandas(**filtros) as task:
        log = task.run()
    return log
