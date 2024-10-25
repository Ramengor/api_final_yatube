"""Модуль с пользовательскими разрешениями для API."""
from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Разрешение, позволяющее изменять объект только его автору."""

    def has_object_permission(self, request, view, obj):
        """Проверяет, имеет ли пользователь разрешение на доступ."""
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)
