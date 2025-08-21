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
    path('dashboard/institute/classes/', TemplateView.as_view(template_name="frontend/institute_classes.html")),
    path('dashboard/institute/classes/add/', TemplateView.as_view(template_name="frontend/add_classes.html")),
    path('dashboard/institute/classes/<int:cls_id>/',
         TemplateView.as_view(template_name='frontend/classroom_exams.html'), name='classroom_exams'),
    path('dashboard/institute/classes/<int:class_id>/classes/add/',
         TemplateView.as_view(template_name="frontend/add_classes.html")),
    path('dashboard/institute/classes/<int:class_id>/exams/add/',
         TemplateView.as_view(template_name="frontend/add_exams.html")),
    path(
        'dashboard/institute/categories/add/',
        TemplateView.as_view(template_name="frontend/add_categories.html"),
        name='add_category'
    ),
    path(
        'dashboard/institute/classes/<int:class_id>/edit/',
        TemplateView.as_view(template_name="frontend/edit_classes.html"),
        name='edit_classroom'
    ),
    path(
        'dashboard/institute/classes/<int:class_id>/students/',
        TemplateView.as_view(template_name="frontend/student_classroom.html"),
        name='student_classroom'
    ),
    path(
        'dashboard/institute/classes/<int:class_id>/students/add/',
        TemplateView.as_view(template_name="frontend/add_student_classroom.html"),
        name='add_student_classroom'
    ),
    path(
        'dashboard/institute/classes/<int:class_id>/exams/<int:exam_id>/questions/',
        TemplateView.as_view(template_name="frontend/questions.html"),
        name='exam_detail'
    ),
    path(
        "dashboard/institute/classes/<int:classroom_id>/exams/<int:exam_id>/add-question/",
        TemplateView.as_view(template_name="frontend/add_question.html"),
        name='exam_detail'
    ),

]
