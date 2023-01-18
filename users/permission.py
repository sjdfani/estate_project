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


class Is_Admin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated and request.user.role == Role.ADMIN
        )


class Is_Advisor(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated and request.user.role == Role.ADVISOR
        )


class Is_User(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated and request.user.role == Role.USER
        )


class Is_Manager_OR_Assistant(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated and (
                request.user.role == Role.MANAGER or request.user.role == Role.ASSISTANT)
        )


class Is_Any_Access_Except_Advisor(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated and not (
                request.user.role == Role.ADVISOR)
        )


class Is_Manager_OR_Assistant_OR_Advisor(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated and (
                request.user.role in [Role.MANAGER, Role.ASSISTANT, Role.ADVISOR])
        )


class Is_Manager_OR_Assistant_OR_Admin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated and (
                request.user.role in [Role.MANAGER, Role.ASSISTANT, Role.ADMIN])
        )


class Is_Manager_OR_Assistant_OR_User(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated and (
                request.user.role in [Role.MANAGER, Role.ASSISTANT, Role.USER])
        )
