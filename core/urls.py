from django.urls import path
from core import views
from dj_rest_auth.views import LogoutView

urlpatterns = [
    path('auth/signup/admin/', views.AdminSignUpAPIView.as_view(), name='admin_signup'),
    path('auth/signup/institute/', views.InstituteSignUpAPIView.as_view(), name='institute_signup'),
    path('auth/signup/teacher/', views.TeacherSignUpAPIView.as_view(), name='teacher_signup'),
    path('auth/signup/student/', views.StudentSignUpAPIView.as_view(), name='student_signup'),

    path('auth/login/', views.CustomLoginView.as_view(), name='custom_login'),
    path('auth/logout/', LogoutView.as_view(), name='custom_logout'),

    path('institutes/', views.InstituteListAPIView.as_view(), name='institute'),
    path('institutes/<int:pk>/', views.InstituteRetrieveUpdateDeleteAPIView.as_view(), name='institute-detail'),

    path('teachers/', views.TeacherListAPIView.as_view(), name='teacher'),
    path('teachers/<int:pk>/', views.TeacherRetrieveUpdateDeleteAPIView.as_view(), name='teacher-detail'),

    path('students/', views.StudentListAPIView.as_view(), name='student'),
    path('students/<int:pk>/', views.StudentRetrieveUpdateDeleteAPIView.as_view(), name='student-detail'),

]
