from django.urls import path
from core import views
from dj_rest_auth.views import LogoutView

urlpatterns = [
    # path('auth/signup/team/', views.TeamSignUpAPIView.as_view(), name='team_signup'),
    # path('auth/signup/staff/', views.StaffSignUpAPIView.as_view(), name='staff_signup'),
    # path('auth/login/', views.CustomLoginView.as_view(), name='custom_login'),
    # path('auth/logout/', LogoutView.as_view(), name='custom_logout'),
    # path('users/<int:pk>/', views.CustomUserDetailView.as_view(), name='user_detail'),
]
