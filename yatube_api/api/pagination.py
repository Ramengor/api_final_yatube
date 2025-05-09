"""Модуль для кастомной пагинации в API."""
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class PostPagination(LimitOffsetPagination):
    """Класс кастомной пагинации для постов."""

    def get_paginated_response(self, data):
        """Возвращает пагинированный ответ с результатами."""
        if ('limit' in self.request.query_params
                or 'offset' in self.request.query_params):
            return Response({
                'count': self.count,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'results': data
            })
        return Response(data)
