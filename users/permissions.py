from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Проверка на администратора"""

    def has_permission(self, request, view):
        return request.user.role == "admin"


class IsAuthor(BasePermission):
    """Проверка на автора объекта"""

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
