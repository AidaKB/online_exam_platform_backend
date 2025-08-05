from dj_rest_auth.views import LoginView
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrInstituteSelf, IsAdminOrTeacherSelf, IsAdminOrStudentOrInstituteSelf
from core import serializers, filters
from . import models
from .serializers import CustomLoginSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class AdminSignUpAPIView(generics.CreateAPIView):
    serializer_class = serializers.AdminSignUpSerializer


class InstituteSignUpAPIView(generics.CreateAPIView):
    serializer_class = serializers.InstituteSignUpSerializer


class InstituteListAPIView(generics.ListAPIView):
    serializer_class = serializers.InstituteSerializer
    queryset = models.Institute.objects.all()
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.InstituteFilter

    search_fields = ['name', 'registration_code', 'phone', 'account__email']
    ordering_fields = ['name', 'created_at']
    ordering = ['-created_at']


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
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.TeacherFilter

    search_fields = ['account__email', 'account__first_name', 'account__last_name', 'expertise', 'national_code']
    ordering_fields = ['created_at', 'account__first_name']
    ordering = ['-created_at']

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


class StudentListAPIView(generics.ListAPIView):
    serializer_class = serializers.StudentSerializer
    queryset = models.Student.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.StudentFilter

    search_fields = ['account__first_name', 'account__last_name', 'account__email', 'national_code', 'phone_number']
    ordering_fields = ['created_at', 'date_of_birth', 'account__first_name']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user

        if getattr(user, 'user_type', None) == 'admin':
            return models.Student.objects.all()

        if hasattr(user, 'institute'):
            return models.Student.objects.filter(institute=user.institute)

        raise PermissionDenied("شما مجاز به مشاهده لیست دانشجویان نیستید.")


class StudentRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAdminOrStudentOrInstituteSelf()]

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        user = self.request.user

        if getattr(user, "user_type", None) == "admin":
            return obj

        if hasattr(user, "student") and user.student.id == obj.id:
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
                {"detail": "این دانش قابل حذف نیست چون اطلاعاتی وابسته به آن وجود دارند."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.CustomUserDetailSerializer
    permission_classes = [IsAuthenticated]


@method_decorator(csrf_exempt, name='dispatch')
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
