from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomizedPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response(
            {
                'meta': {
                    'total_items': self.page.paginator.count,
                    'page_size': self.page_size,
                    'next': self.get_next_link(),
                    'previous': self.get_previous_link(),
                    'current': self.page.number,
                    'last': self.page.paginator.num_pages,
                },
                'results': data,
            }
        )
