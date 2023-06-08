from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 7
    page_size_query_param = 'page_size'
    max_page_size = 7

    def get_paginated_response(self, data):
        print(self.page.paginator.num_pages, "Countttttt")
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'results': data,
            'current_page_number': self.page.number
        })
