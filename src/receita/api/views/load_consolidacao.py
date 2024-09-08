import os

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ...tasks import (LoadConsolidacao, LoadConsolidacaoPandas,
                      load_consolidacao_async, load_consolidacao_pandas_async)


class LoadConsolidacaoView(APIView):
    """View que aciona a task de construção da base de [Consolidacao]"""

    def post(self, request, *args, **kwargs) -> Response:
        filtros = {
            'data_range': (request.data.get('data_inicio'), request.data.get('data_fim')),
            'vendedor_list': request.data.get('vendedor', []),
            'loja_list': request.data.get('loja', []),
            'equipe_venda_list': request.data.get('equipe_venda', []),
            'produto_list': request.data.get('produto', [])
        }

        with LoadConsolidacaoPandas(**filtros) as load:
            log_pandas = load.run()
        with LoadConsolidacao(**filtros) as load:
            log_polars = load.run()

        faster = min(log_pandas.get('duration_transform'),
                     log_polars.get('duration_transform'))
        slower = max(log_pandas.get('duration_transform'),
                     log_polars.get('duration_transform'))
        percentage_diff = round(((slower - faster) / slower) * 100, 2)

        if faster == log_pandas.get('duration_transform'):
            faster_library = "Pandas"
        else:
            faster_library = "Polars"

        log_data = {
            'log_pandas': log_pandas,
            'log_polars': log_polars,
            'Comparativo:': f'O {faster_library} é {percentage_diff}% mais rápido para esta quantidade de dados'
        }

        project_root = os.path.dirname(os.path.abspath(__file__))
        log_file_path = os.path.join(
            project_root, f'log_consolidacao.txt')

        with open(log_file_path, 'w') as log_file:
            for key, value in log_data.items():
                log_file.write(f'{key}: {value}\n')

        return Response(log_data)

        load_consolidacao_async.delay()
        return Response(
            {"message": "A requisição foi recebida e a carga foi iniciada!"},
            status=status.HTTP_202_ACCEPTED)
