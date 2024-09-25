from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from ..models import Venda
from ..tasks import load_consolidacao_async


@receiver([post_save, post_delete], sender=Venda)
def changes_venda(sender, instance, created=False, *args, **kwargs):
    params = {
        "data_range":[instance.data.strftime("%Y-%m-%d"), instance.data.strftime("%Y-%m-%d")],
        "produto_list": [instance.produto.id],
        "vendedor_list": [instance.vendedor.id],
    }
    load_consolidacao_async.delay(filtros=params)
