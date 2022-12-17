from rest_framework.permissions import (SAFE_METHODS, BasePermission)


class AuthorStaffOrReadOnly(BasePermission):
    """
    Класс разрешений для служебного персонала и автора.
    Остальным только чтение объекта.
    """
    def has_object_permission(self, request, view, obj):
        return (
            (request.method in SAFE_METHODS)
            or (request.user == obj.author)
            or request.user.is_staff
        )
