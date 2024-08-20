from rest_framework import permissions


class IsOwnerOfCourse(permissions.BasePermission):
    '''
    Is requested user the owner of the course
    '''
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class IsOwnerOfGroup(permissions.BasePermission):
    '''
    Is requested user the owner of the group
    '''
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.course.author == request.user


class IsOwnerOfLesson(permissions.BasePermission):
    '''
    Is requested user the owner of the lesson
    '''
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.course.author == request.user
    