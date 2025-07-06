from dj_rest_auth.views import LoginView
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrInstituteSelf, IsAdminOrTeacherSelf
from core import serializers
from . import models
from .serializers import CustomLoginSerializer


class AdminSignUpAPIView(generics.CreateAPIView):
    serializer_class = serializers.AdminSignUpSerializer


class InstituteSignUpAPIView(generics.CreateAPIView):
    serializer_class = serializers.InstituteSignUpSerializer


class InstituteListAPIView(generics.ListAPIView):
    serializer_class = serializers.InstituteSerializer
    queryset = models.Institute.objects.all()
    permission_classes = [permissions.IsAdminUser]


class InstituteRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Institute.objects.all()
    serializer_class = serializers.InstituteSerializer

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        user = self.request.user

        if getattr(user, "user_type", None) == "admin":
            return obj

        if hasattr(user, "institute") and user.institute.id == obj.id:
            return obj

        raise PermissionDenied("شما مجاز به مشاهده یا ویرایش این موسسه نیستید.")

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAdminOrInstituteSelf()]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
        except ProtectedError:
            return Response(
                {"detail": "این موسسه قابل حذف نیست چون کلاس‌هایی وابسته به آن وجود دارند."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(status=status.HTTP_204_NO_CONTENT)


class TeacherSignUpAPIView(generics.CreateAPIView):
    serializer_class = serializers.TeacherSignUpSerializer


class TeacherListAPIView(generics.ListAPIView):
    serializer_class = serializers.TeacherSerializer
    queryset = models.Teacher.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if getattr(user, 'user_type', None) == 'admin':
            return models.Teacher.objects.all()

        if hasattr(user, 'institute'):
            return models.Teacher.objects.filter(institute=user.institute)

        raise PermissionDenied("شما مجاز به مشاهده لیست استادها نیستید.")


class TeacherRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Teacher.objects.all()
    serializer_class = serializers.TeacherSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAdminOrTeacherSelf()]

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        user = self.request.user

        if getattr(user, "user_type", None) == "admin":
            return obj

        if hasattr(user, "teacher") and user.teacher.id == obj.id:
            return obj

        if hasattr(user, "institute") and obj.institute.id == user.institute.id:
            return obj

        raise PermissionDenied("شما مجاز به مشاهده یا ویرایش این اطلاعات نیستید.")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
        except ProtectedError:
            return Response(
                {"detail": "این معلم قابل حذف نیست چون کلاس‌هایی وابسته به آن وجود دارند."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(status=status.HTTP_204_NO_CONTENT)


class StudentSignUpAPIView(generics.CreateAPIView):
    serializer_class = serializers.StudentSignUpSerializer


class CustomLoginView(LoginView):
    serializer_class = CustomLoginSerializer

    def get_response(self):
        original_response = super().get_response()
        user = self.user
        data = original_response.data
        data['user_id'] = user.id
        return Response(data)

# class CustomUserDetailView(generics.RetrieveAPIView):
#     queryset = get_user_model().objects.all()
#     serializer_class = CustomStaffUserSerializer
#     permission_classes = [permissions.IsAuthenticated]
