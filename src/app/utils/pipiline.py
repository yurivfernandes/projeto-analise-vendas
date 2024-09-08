from django.utils import timezone


class Pipeline:
    """Classe padrão que generaliza os métodos de todas as Pipelines de dados"""

    def __init__(self, **kwargs):
        self.log = {
            'n_inserted': 0,
            'n_deleted': 0,
            'started_at': timezone.now(),
            'finished_at': None,
            'duration': None
        }

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.log['finished_at'] = timezone.now()
        self.log['duration'] = (
            self.log['finished_at'] -
            self.log['started_at']).total_seconds()
