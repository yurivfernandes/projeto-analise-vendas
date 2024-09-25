from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1_000

    def get_paginated_response(self, data) -> Response:
        return Response(
            {
                'count': self.page.paginator.count,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'total_pages': self.page.paginator.num_pages,
                'results': data,
            }
        )
    

class CustomLargePagination(CustomPagination):
    page_size = 1_000
    max_page_size = 10_000