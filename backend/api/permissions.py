from rest_framework.permissions import (SAFE_METHODS, BasePermission,
                                        IsAuthenticatedOrReadOnly)

# class AuthorStaffOrReadOnly(IsAuthenticatedOrReadOnly):
#     """
#     Класс разрешений для служебного персонала и автора.
#     Остальным только чтение объекта.
#     """
#     def has_object_permission(self, request, view, obj):
#         return (
#             request.method in (SAFE_METHODS,)
#             or (request.user == obj.author)
#             or request.user.is_staff
#         )
#
#
# class AdminOrReadOnly(BasePermission):
#     """
#     Класс разрешений на создание и изменение только для админов.
#     Остальным только чтение.
#     """
#     def has_permission(self, request, view):
#         return (
#             request.method in (SAFE_METHODS,)
#             or request.user.is_authenticated
#             and request.user.is_staff
#         )


class Testp(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or obj.author == request.user)


# class OwnerUserOrReadOnly(IsAuthenticatedOrReadOnly):
#     """
#     Класс разрешений на изменение только для админа и пользователя.
#     Остальным только чтение объекта.
#     """
#     def has_object_permission(self, request, view, obj):
#         return (
#             request.method in (SAFE_METHODS,)
#             or (request.user == obj)
#             or request.user.is_staff
#         )
#

# class IsAdminOrReadOnly(permissions.BasePermission):
#     """Gives an oppurtunity to change data only to superuser."""
#     def has_permission(self, request, view):
#         """Gives an oppurtunity to 'POST' only to authorized admins."""
#         return (request.method in permissions.SAFE_METHODS
#                 or (request.user.is_authenticated and (
#                     request.user.is_admin or request.user.is_superuser)))
#
#     def has_object_permission(self, request, view, obj):
#         """Gives an oppurtunity to 'PUT', 'PATCH' or 'DELETE' only to:
#            admin or superuser."""
#         return (request.method in permissions.SAFE_METHODS
#                 or request.user.is_admin or request.user.is_superuser)
#
#
class IsAuthorOrReadOnly(BasePermission):
    """Gives an oppurtunity to change data only to author."""
    def has_object_permission(self, request, view, obj):
        """Gives an oppurtunity to 'PUT', 'PATCH' or 'DELETE'
           only to author."""
        return (request.method in SAFE_METHODS
                or obj.author == request.user)

#
# class IsModeratorOrReadOnly(permissions.BasePermission):
#     """Gives an oppurtunity to change data only to moderator."""
#     def has_object_permission(self, request, view, obj):
#         """Gives an oppurtunity to 'PUT', 'PATCH' or 'DELETE'
#            only to moderator."""
#         return (request.method in permissions.SAFE_METHODS
#                 or request.user.is_moderator)
