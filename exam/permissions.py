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


class IsAdminOrTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return getattr(user, 'user_type', None) in ['admin', 'teacher']

class IsAdminOrTeacherOrInstituteOwner(permissions.BasePermission):
    """
    فقط ادمین، استاد مربوط به کلاس یا موسسه‌ای که آن استاد متعلق به آن است می‌توانند آپدیت و دیلیت کنند.
    همه کاربران احراز هویت شده می‌توانند گت کنند.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        # همه می‌تونن گت کنن
        if request.method in permissions.SAFE_METHODS:
            return True

        # ادمین دسترسی کامل دارد
        if getattr(user, 'user_type', None) == 'admin':
            return True

        # اگر استاد خودش باشد
        if hasattr(user, 'teacher') and obj.teacher == user.teacher:
            return True

        # اگر موسسه استاد باشد
        if hasattr(user, 'institute') and obj.teacher and obj.teacher.institute == user.institute:
            return True

        return False