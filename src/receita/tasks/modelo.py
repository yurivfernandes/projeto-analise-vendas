import pandas as pd
from celery import shared_task
from django.db import transaction
from django.db.models import QuerySet

from app.utils.pipiline import Pipeline

from ..models import Consolidacao
from ..utils import Mixin


class LoadConsolidacao(Pipeline, Mixin):
    """Extrai, transforma e carrega os dados de Receita Consolidados."""

    def get_consolidacao_queryset(self) -> QuerySet:
        return (
            super().get_consolidacao_queryset()
            .filter())

    def get_imposto_queryset(self) -> QuerySet:
        return (
            super().get_imposto_queryset()
            .filter())

    def get_receita_tipo_queryset(self) -> QuerySet:
        return (
            super().get_receita_tipo_queryset()
            .filter())

    def get_venda_queryset(self) -> QuerySet:
        return (
            super().get_venda_queryset()
            .filter())

    def __init__(self, **kwargs) -> None:
        super().__init__()

    def run(self) -> dict:
        self.extract_transform_dataset()
        self.load()
        return self.log

    def extract_transform_dataset(self) -> None:
        self.dataset = pd.DataFrame()

    @transaction.atomic
    def load(self) -> None:
        self._delete()
        self._save()

    def _delete(self):
        objs = self.get_consolidacao_queryset()
        if objs.exists():
            self.log['n_deleted'], __ = objs.delete()

    def _save(self):
        if self.dataset.empty:
            return

        objs = [
            Consolidacao(**vals)
            for vals in
            self.dataset.to_dict('records')]
        bulk = (
            Consolidacao
            .objects
            .bulk_create(
                objs=objs,
                batch_size=1000))
        self.log['n_inserted'] = len(bulk)


@shared_task(
    name='receita.load_consolidacao',
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={'max_retries': 3})
def load_consolidacao_async() -> dict:
    with LoadConsolidacao() as task:
        log = task.run()
    return log
