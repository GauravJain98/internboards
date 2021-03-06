from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

class BasicPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    max_page_size = 20
    
    def get_paginated_response(self, data):
        return Response({
            'count':len(data),
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'results': data
        })