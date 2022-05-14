from rest_framework.permissions import SAFE_METHODS
from rest_framework import permissions


class ReadOnly(permissions.BasePermission):
    """Доступ только для чтения."""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class AdminRoleOnly(permissions.BasePermission):
    """Класс разрешений для полного доступа
    к представлению только у админа или суперюзера."""

    def has_permission(self, request, view):
        """Функция для проверки разрешения на уровне представления."""

        return (request.user.is_authenticated
                and request.user.role in ('admin')
                or request.user.is_superuser)


class IsAuthorModeratorAdminOrReadOnly(permissions.BasePermission):
    """Класс разрешений для доступа к представлению автору,
    моредатору, администратору и суперюзеру."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or bool(request.user and request.user.is_authenticated))

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and request.user.role in ('admin', 'moderator')
                or request.user.is_superuser
                or obj.author == request.user)
