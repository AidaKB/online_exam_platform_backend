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

        if request.method in permissions.SAFE_METHODS:
            return True

        if getattr(user, 'user_type', None) == 'admin':
            return True

        if hasattr(user, 'teacher') and obj.teacher == user.teacher:
            return True

        if hasattr(user, 'institute') and obj.teacher and obj.teacher.institute == user.institute:
            return True

        return False


class IsAdminOrInstituteOrCreatorTeacher(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user

        if request.method in permissions.SAFE_METHODS:
            return True

        if user.user_type == 'admin':
            return True

        if hasattr(user, 'institute'):
            return obj.classroom.teacher.institute_id == user.institute.id

        if hasattr(user, 'teacher'):
            return obj.classroom.teacher.institute_id == user.teacher.institute_id

        return False


class IsAdminOrInstituteOrTeacherForQuestion(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == 'POST':
            return user.user_type == 'admin' or hasattr(user, 'teacher') or hasattr(user, 'institute')

        return True

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.user_type == 'admin':
            return True

        if hasattr(user, 'institute'):
            return obj.exam.classroom.teacher.institute == user.institute

        if hasattr(user, 'teacher'):
            return obj.exam.classroom.teacher == user.teacher

        if hasattr(user, 'student') and request.method in permissions.SAFE_METHODS:
            return obj.exam.classroom.teacher.institute == user.student.institute

        return False


class OptionPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == "POST":
            return (
                    user.is_superuser or
                    hasattr(user, 'teacher') or
                    hasattr(user, 'institute')
            )

        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return (
                    user.is_superuser or
                    hasattr(user, 'teacher') or
                    hasattr(user, 'institute')
            )

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        exam = obj.question.exam

        if request.method in permissions.SAFE_METHODS:
            if user.is_superuser:
                return True
            if hasattr(user, 'teacher') and exam.classroom.teacher == user.teacher:
                return True
            if hasattr(user, 'institute') and exam.classroom.teacher.institute == user.institute:
                return True
            if hasattr(user, 'student') and exam.classroom.teacher.institute == user.student.institute:
                return True
            return False

        else:
            if user.is_superuser:
                return True
            if hasattr(user, 'teacher') and exam.classroom.teacher == user.teacher:
                return True
            if hasattr(user, 'institute') and exam.classroom.teacher.institute == user.institute:
                return True
            return False


class UserAnswerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        if request.method == "POST":
            return user.is_superuser or hasattr(user, 'student')

        if request.method in permissions.SAFE_METHODS or request.method in ["PUT", "PATCH"]:
            return (
                    user.is_superuser or
                    hasattr(user, 'student') or
                    hasattr(user, 'teacher') or
                    hasattr(user, 'institute')
            )

        if request.method == "DELETE":
            return user.is_superuser

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user

        if request.method in permissions.SAFE_METHODS or request.method in ["PUT", "PATCH"]:
            if user.is_superuser:
                return True
            if hasattr(user, 'student') and obj.user == user.student:
                return True
            if hasattr(user, 'teacher') and obj.question.exam.classroom.teacher == user.teacher:
                return True
            if hasattr(user, 'institute') and obj.question.exam.classroom.teacher.institute == user.institute:
                return True

        if request.method == "DELETE":
            return user.is_superuser

        return False
