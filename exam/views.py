from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
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

        elif hasattr(user, 'institute') and classroom.institute == user.institute:
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
        user = self.request.user

        if hasattr(user, 'teacher'):
            serializer.save(creator=user)
        elif hasattr(user, 'institute'):
            serializer.save(creator=user)
        elif user.user_type == 'admin':
            serializer.save(creator=user)
        else:
            raise PermissionDenied("شما اجازه ساخت آزمون را ندارید.")


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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.Question.objects.select_related('exam__classroom__teacher__institute')

    def get_object(self):
        user = self.request.user
        question = super().get_object()
        exam = question.exam
        classroom = exam.classroom
        teacher = classroom.teacher
        institute = teacher.institute

        if hasattr(user, 'student'):
            if institute == user.student.institute:
                if self.request.method in ('GET',):
                    return question
                raise PermissionDenied("دانش‌آموز فقط می‌تواند سوالات آزمون خود را مشاهده کند.")

        elif hasattr(user, 'teacher'):
            if teacher == user.teacher:
                return question
            raise PermissionDenied("شما فقط به سوالات آزمون‌های خودتان دسترسی دارید.")

        elif hasattr(user, 'institute'):
            if institute == user.institute:
                return question
            raise PermissionDenied("این سوال متعلق به موسسه شما نیست.")

        elif getattr(user, 'user_type', None) == 'admin':
            return question

        raise PermissionDenied("شما اجازه مشاهده یا ویرایش این سوال را ندارید.")
