from rest_framework.permissions import BasePermission
from rest_framework.pagination import PageNumberPagination
from online_cinema.models import Cinema
from rest_framework.response import Response


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user

from math import ceil

class CinemaPagination(PageNumberPagination):
    page_size = 2
    max_page_size = ceil( len( Cinema.objects.all()) / 2 )

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })

