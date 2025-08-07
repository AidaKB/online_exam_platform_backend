from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/institute/', TemplateView.as_view(template_name='frontend/institute_signup.html'),
         name='signup_institute'),
    path('login/', views.login_view, name='login'),

    path('dashboard/institute/', views.institute_dashboard, name='institute_dashboard'),
    path('dashboard/institute/profile/', TemplateView.as_view(template_name='frontend/institute_profile.html'),
         name='institute-profile'),

]
