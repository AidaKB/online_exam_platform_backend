# permissions.py
from rest_framework import permissions


class IsAdminOrInstituteSelf(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user

        if getattr(user, 'user_type', None) == 'admin':
            return True

        if hasattr(user, 'institute'):
            return obj.id == user.institute.id

        return False


class IsAdminOrTeacherSelf(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user

        if getattr(user, 'user_type', None) == 'admin':
            return True

        if hasattr(user, 'teacher'):
            return obj.id == user.teacher.id

        if hasattr(user, 'institute'):
            return obj.institute.id == user.institute.id

        return False


class IsAdminOrStudentOrInstituteSelf(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user

        if getattr(user, 'user_type', None) == 'admin':
            return True

        if hasattr(user, 'student'):
            return obj.id == user.student.id

        if hasattr(user, 'institute'):
            return obj.institute.id == user.institute.id

        return False
