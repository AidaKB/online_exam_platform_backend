from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated , IsAdminUser
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
            return models.Classroom.objects.filter(institute=user.institute)
        else:
            return models.Classroom.objects.all()

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), permissions.IsTeacherOrInstituteOrAdmin()]
        return [IsAuthenticated()]


class ClassroomRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.ClassroomSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        classroom_id = self.kwargs.get('pk')
        classroom = get_object_or_404(models.Classroom, pk=classroom_id)

        if getattr(user, "user_type", None) == "admin":
            return classroom

        elif hasattr(user, "teacher") and classroom.teacher == user.teacher:
            return classroom

        elif hasattr(user, "institute") and classroom.institute == user.institute:
            return classroom

        raise PermissionDenied("شما اجازه دسترسی به این کلاس را ندارید.")


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


class StudentClassroomRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
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
            if obj.classroom.institute_id == user.institute.id:
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


class MajorRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Major.objects.all()
    serializer_class = serializers.MajorSerializer
    permission_classes = [IsAdminUser]


