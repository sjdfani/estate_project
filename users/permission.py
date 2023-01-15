from rest_framework.permissions import BasePermission


class Is_Manager(BasePermission):
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated and request.user.is_manager)


class Is_Admin(BasePermission):
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated and request.user.is_admin)


class Is_Adviser(BasePermission):
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated and request.user.is_adviser)


class Is_User(BasePermission):
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated and request.user.is_user)
