
from django.db.models import QuerySet

from ..models import Consolidacao, Imposto, ImpostoTipo, Tipo, Venda


class Mixin:
    """Mixin com métodos genéricos para serem reaproveitados nas apis e tasks"""

    def get_consolidacao_queryset(self) -> QuerySet:
        """Retorna um queryset com os dados de [Consolidacao]"""
        return (
            Consolidacao
            .objects)

    def get_imposto_tipo_queryset(self) -> QuerySet:
        """Retorna um queryset com os dados de [ImpostoTipo]"""
        return (
            ImpostoTipo
            .objects)

    def get_imposto_queryset(self) -> QuerySet:
        """Retorna um queryset com os dados de [Imposto]"""
        return (
            Imposto
            .objects)

    def get_receita_tipo_queryset(self) -> QuerySet:
        """Retorna um queryset com os dados de [Tipo]"""
        return (
            Tipo
            .objects)

    def get_venda_queryset(self) -> QuerySet:
        """Retorna um queryset com os dados de [Venda]"""
        return (
            Venda
            .objects)
