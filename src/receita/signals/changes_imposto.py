from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from ..models import Imposto
from ..tasks import load_consolidacao_async


@receiver([post_save, post_delete], sender=Imposto)
def changes_imposto(sender, instance, created=False, *args, **kwargs):
    params = {
        "loja_list": [instance.loja.id],
    }
    load_consolidacao_async.delay(filtros=params)
