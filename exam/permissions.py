from rest_framework import permissions


class IsTeacherOrInstituteOrAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return (
                hasattr(user, "teacher") or
                hasattr(user, "institute") or
                getattr(user, "user_type", None) == "admin"
        )


class IsStudentOfClassOrTeacherOrInstitute(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, "teacher"):
            return obj.teacher == request.user.teacher
        elif hasattr(request.user, "institute"):
            return obj.institute == request.user.institute
        elif hasattr(request.user, "student"):
            return obj.student_classroom.filter(student=request.user.student).exists()
        return False
