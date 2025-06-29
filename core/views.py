from dj_rest_auth.views import LoginView
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response

from core import serializers
from .serializers import CustomLoginSerializer


class AdminSignUpAPIView(generics.CreateAPIView):
    serializer_class = serializers.AdminSignUpSerializer


class InstituteSignUpAPIView(generics.CreateAPIView):
    serializer_class = serializers.InstituteSignUpSerializer


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
