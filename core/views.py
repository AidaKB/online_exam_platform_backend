from dj_rest_auth.views import LoginView
from django.db.models import ProtectedError
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrInstituteSelf
from core import serializers
from .models import Institute
from .serializers import CustomLoginSerializer


class AdminSignUpAPIView(generics.CreateAPIView):
    serializer_class = serializers.AdminSignUpSerializer


class InstituteSignUpAPIView(generics.CreateAPIView):
    serializer_class = serializers.InstituteSignUpSerializer


class InstituteListAPIView(generics.ListAPIView):
    serializer_class = serializers.InstituteSerializer
    queryset = Institute.objects.all()
    permission_classes = [permissions.IsAdminUser]


class InstituteRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Institute.objects.all()
    serializer_class = serializers.InstituteSerializer

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
