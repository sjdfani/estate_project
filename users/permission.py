from rest_framework.permissions import BasePermission
from .models import Role


class Is_Manager(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated and request.user.role == Role.MANAGER
        )


class Is_Assistant(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated and request.user.role == Role.ASSISTANT
        )


class Is_Manager_OR_Assistant(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated and (
                request.user.role == Role.MANAGER or request.user.role == Role.ASSISTANT)
        )


class Is_Admin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated and request.user.role == Role.ADMIN
        )


class Is_Adviser(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated and request.user.role == Role.ADVISER
        )


class Is_User(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated and request.user.role == Role.USER
        )
