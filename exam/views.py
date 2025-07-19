from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from . import models
from . import serializers
from . import permissions
from .models import Major


class ClassroomListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.ClassroomSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "student"):
            return models.Classroom.objects.filter(student_classroom__student=user.student)
        elif hasattr(user, "teacher"):
            return models.Classroom.objects.filter(teacher=user.teacher)
        elif hasattr(user, "institute"):
            return models.Classroom.objects.filter(teacher__institute=user.institute)
        else:
            return models.Classroom.objects.all()

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), permissions.IsTeacherOrInstituteOrAdmin()]
        return [IsAuthenticated()]


class ClassroomDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Classroom.objects.all()
    serializer_class = serializers.ClassroomSerializer
    permission_classes = [IsAuthenticated, permissions.IsAdminOrTeacherOrInstituteOwner]


class StudentClassroomListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.StudentClassroomSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if getattr(user, 'user_type', None) == 'admin':
            return models.StudentClassroom.objects.all()

        elif hasattr(user, 'institute'):
            return models.StudentClassroom.objects.filter(classroom__institute=user.institute)

        elif hasattr(user, 'teacher'):
            return models.StudentClassroom.objects.filter(classroom__teacher=user.teacher)

        elif hasattr(user, 'student'):
            return models.StudentClassroom.objects.filter(student=user.student)

        return models.StudentClassroom.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        classroom = serializer.validated_data['classroom']

        if getattr(user, 'user_type', None) == 'admin':
            serializer.save()

        elif hasattr(user, 'institute') and classroom.teacher.institute == user.institute:
            serializer.save()

        elif hasattr(user, 'teacher') and classroom.teacher == user.teacher:
            serializer.save()

        else:
            raise PermissionDenied("شما اجازه افزودن دانش‌آموز به این کلاس را ندارید.")


class StudentClassroomDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.StudentClassroomSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        obj = get_object_or_404(models.StudentClassroom, pk=self.kwargs["pk"])

        if getattr(user, 'user_type', None) == 'admin':
            return obj

        if hasattr(user, 'student'):
            if self.request.method == 'GET' and obj.student_id == user.student.id:
                return obj
            raise PermissionDenied("دانش‌آموز فقط می‌تواند پاسخ‌های خودش را مشاهده کند.")

        if hasattr(user, 'institute'):
            if obj.classroom.teacher.institute_id == user.institute.id:
                return obj
            raise PermissionDenied("این کلاس متعلق به موسسه شما نیست.")

        if hasattr(user, 'teacher'):
            if obj.classroom.teacher_id == user.teacher.id:
                return obj
            raise PermissionDenied("شما استاد این کلاس نیستید.")

        raise PermissionDenied("شما مجاز به انجام این عملیات نیستید.")


class MajorListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.MajorSerializer
    permission_classes = [IsAuthenticated]
    queryset = Major.objects.all()


class MajorDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Major.objects.all()
    serializer_class = serializers.MajorSerializer
    permission_classes = [IsAdminUser]


class ExamCategoryListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.ExamCategorySerializer

    def get_queryset(self):
        user = self.request.user

        if user.user_type == 'admin':
            return models.ExamCategory.objects.all()

        elif hasattr(user, 'teacher'):
            return models.ExamCategory.objects.filter(
                Q(creator=user) | Q(creator__user_type='admin')
            )

        return models.ExamCategory.objects.none()

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), permissions.IsAdminOrTeacher()]
        return [IsAuthenticated()]


class ExamCategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.ExamCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'admin':
            return models.ExamCategory.objects.all()
        elif hasattr(user, 'teacher'):
            return models.ExamCategory.objects.filter(
                Q(creator=user) | Q(creator__user_type='admin')
            )
        return models.ExamCategory.objects.none()

    def perform_update(self, serializer):
        user = self.request.user
        instance = self.get_object()

        if user.user_type == 'admin' or instance.creator == user:
            serializer.save()
        else:
            raise PermissionDenied("شما مجاز به ویرایش این دسته‌بندی نیستید.")

    def perform_destroy(self, instance):
        user = self.request.user

        if user.user_type == 'admin' or instance.creator == user:
            instance.delete()
        else:
            raise PermissionDenied("شما مجاز به حذف این دسته‌بندی نیستید.")


class ExamListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.ExamSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.user_type == 'admin':
            return models.Exam.objects.all()

        elif hasattr(user, 'institute'):
            return models.Exam.objects.filter(
                classroom__teacher__institute=user.institute
            )

        elif hasattr(user, 'teacher'):
            return models.Exam.objects.filter(
                classroom__teacher=user.teacher
            )

        elif hasattr(user, 'student'):
            return models.Exam.objects.filter(
                classroom__teacher__institute=user.student.institute
            ).distinct()

        return models.Exam.objects.none()

    def perform_create(self, serializer):
        serializer.save()


class ExamDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Exam.objects.all()
    serializer_class = serializers.ExamSerializer
    permission_classes = [IsAuthenticated, permissions.IsAdminOrInstituteOrCreatorTeacher]


class QuestionListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.QuestionSerializer
    permission_classes = [IsAuthenticated, permissions.IsAdminOrInstituteOrTeacherForQuestion]

    def get_queryset(self):
        user = self.request.user

        if user.user_type == 'admin':
            return models.Question.objects.all()

        if hasattr(user, 'institute'):
            return models.Question.objects.filter(
                exam__classroom__teacher__institute=user.institute
            )

        if hasattr(user, 'teacher'):
            return models.Question.objects.filter(
                exam__classroom__teacher=user.teacher
            )

        if hasattr(user, 'student'):
            return models.Question.objects.filter(
                exam__classroom__teacher__institute=user.student.institute
            ).distinct()

        return models.Question.objects.none()


class QuestionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.QuestionSerializer
    permission_classes = [IsAuthenticated, permissions.IsAdminOrInstituteOrTeacherForQuestion]

    def get_queryset(self):
        return models.Question.objects.select_related('exam__classroom__teacher__institute')


class OptionListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.OptionSerializer
    permission_classes = [IsAuthenticated, permissions.OptionPermission]

    def get_queryset(self):
        user = self.request.user
        question_id = self.kwargs.get('question_id')
        queryset = models.Option.objects.filter(question_id=question_id)

        if user.is_superuser:
            return queryset

        elif hasattr(user, 'teacher'):
            return queryset.filter(question__exam__classroom__teacher=user.teacher)

        elif hasattr(user, 'institute'):
            return queryset.filter(question__exam__classroom__teacher__institute=user.institute)

        elif hasattr(user, 'student'):
            return queryset.filter(question__exam__classroom__teacher__institute=user.student.institute)

        return models.Option.objects.none()

    def perform_create(self, serializer):
        question_id = self.kwargs.get('question_id')
        try:
            question = models.Question.objects.get(pk=question_id)
        except models.Question.DoesNotExist:
            raise serializers.ValidationError({"question": "سوال مشخص‌شده وجود ندارد."})

        serializer.save(question=question)


class OptionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.OptionSerializer
    permission_classes = [IsAuthenticated, permissions.OptionPermission]

    def get_queryset(self):
        user = self.request.user
        queryset = models.Option.objects.filter(
            question_id=self.kwargs.get('question_id')
        ).select_related('question__exam__classroom__teacher__institute')

        if user.is_superuser:
            return queryset

        elif hasattr(user, 'institute'):
            return queryset.filter(question__exam__classroom__teacher__institute=user.institute)

        elif hasattr(user, 'teacher'):
            return queryset.filter(question__exam__classroom__teacher=user.teacher)

        elif hasattr(user, 'student'):
            return queryset.filter(question__exam__classroom__teacher__institute=user.student.institute)

        return models.Option.objects.none()


class UserAnswerListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.UserAnswer.objects.select_related(
        'question__exam__classroom__teacher__institute', 'user'
    )
    serializer_class = serializers.UserAnswerSerializer
    permission_classes = [permissions.UserAnswerPermission]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return models.UserAnswer.objects.all()

        if hasattr(user, 'institute'):
            return models.UserAnswer.objects.filter(
                question__exam__classroom__teacher__institute=user.institute)

        if hasattr(user, 'teacher'):
            return models.UserAnswer.objects.filter(
                question__exam__classroom__teacher=user.teacher)

        if hasattr(user, 'student'):
            return models.UserAnswer.objects.filter(user=user.student)

        return models.UserAnswer.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        question = serializer.validated_data['question']

        if question.question_type != 'Descriptive':
            raise ValidationError("فقط برای سوالات تشریحی می‌توانید پاسخ ثبت کنید.")

        if hasattr(user, 'student'):
            if question.exam.classroom.teacher.institute != user.student.institute:
                raise ValidationError("شما مجاز به پاسخ به این سوال نیستید.")
            serializer.save(user=user.student)

        elif user.is_superuser:
            if 'user' not in serializer.validated_data:
                raise ValidationError("ادمین باید دانش‌آموز را مشخص کند.")
            serializer.save()

        else:
            raise ValidationError("فقط دانش‌آموز یا ادمین می‌توانند پاسخ ثبت کنند.")


class UserAnswerDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.UserAnswer.objects.select_related(
        'question__exam__classroom__teacher__institute', 'user'
    )
    serializer_class = serializers.UserAnswerSerializer
    permission_classes = [permissions.UserAnswerPermission]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return models.UserAnswer.objects.all()

        if hasattr(user, 'institute'):
            return models.UserAnswer.objects.filter(
                question__exam__classroom__teacher__institute=user.institute)

        if hasattr(user, 'teacher'):
            return models.UserAnswer.objects.filter(
                question__exam__classroom__teacher=user.teacher)

        if hasattr(user, 'student'):
            return models.UserAnswer.objects.filter(user=user.student)

        return models.UserAnswer.objects.none()
