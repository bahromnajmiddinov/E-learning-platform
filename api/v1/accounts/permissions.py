from rest_framework import permissions


class IsOwnerOfAccount(permissions.BasePermission):
    '''
    Is requested user the owner of the account
    '''
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
