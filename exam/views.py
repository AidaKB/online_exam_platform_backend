from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from .models import Classroom
from .serializers import ClassroomSerializer
from .permissions import IsTeacherOrInstituteOrAdmin


class ClassroomListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ClassroomSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "student"):
            return Classroom.objects.filter(student_classroom__student=user.student)
        elif hasattr(user, "teacher"):
            return Classroom.objects.filter(teacher=user.teacher)
        elif hasattr(user, "institute"):
            return Classroom.objects.filter(institute=user.institute)
        else:
            return Classroom.objects.all()

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsTeacherOrInstituteOrAdmin()]
        return [IsAuthenticated()]


class ClassroomRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClassroomSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        classroom_id = self.kwargs.get('pk')
        classroom = get_object_or_404(Classroom, pk=classroom_id)

        if getattr(user, "user_type", None) == "admin":
            return classroom

        elif hasattr(user, "teacher") and classroom.teacher == user.teacher:
            return classroom

        elif hasattr(user, "institute") and classroom.institute == user.institute:
            return classroom

        raise PermissionDenied("شما اجازه دسترسی به این کلاس را ندارید.")
