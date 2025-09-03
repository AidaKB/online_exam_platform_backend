from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/institute/', TemplateView.as_view(template_name='frontend/institute_signup.html'),
         name='signup_institute'),
    path('login/', views.login_view, name='login'),

    path('dashboard/institute/', views.institute_dashboard, name='institute_dashboard'),
    path('dashboard/teacher/', views.teacher_dashboard, name='teacher_dashboard'),

    path(
        'dashboard/institute/profile/',
        TemplateView.as_view(template_name='frontend/institute_profile.html'),
        name='profile'
    ),
    path(
        'dashboard/teacher/profile/',
        TemplateView.as_view(template_name='frontend/teacher_profile.html'),
        name='profile'
    ),
    path(
        'dashboard/<str:user_type>/classes/',
        TemplateView.as_view(template_name="frontend/classes.html"),
        name='classes'
    ),
    path('dashboard/<str:user_type>/classes/add/', TemplateView.as_view(template_name="frontend/add_classes.html")),
    path('dashboard/<str:user_type>/classes/<int:cls_id>/',
         TemplateView.as_view(template_name='frontend/classroom_exams.html'), name='classroom_exams'),
    path('dashboard/<str:user_type>/classes/<int:class_id>/classes/add/',
         TemplateView.as_view(template_name="frontend/add_classes.html")),
    path('dashboard/<str:user_type>/classes/<int:class_id>/exams/add/',
         TemplateView.as_view(template_name="frontend/add_exams.html")),
    path(
        'dashboard/<str:user_type>/categories/add/',
        TemplateView.as_view(template_name="frontend/add_categories.html"),
        name='add_category'
    ),
    path(
        'dashboard/<str:user_type>/classes/<int:class_id>/edit/',
        TemplateView.as_view(template_name="frontend/edit_classes.html"),
        name='edit_classroom'
    ),
    path(
        'dashboard/<str:user_type>/classes/<int:class_id>/students/',
        TemplateView.as_view(template_name="frontend/student_classroom.html"),
        name='student_classroom'
    ),
    path(
        'dashboard/<str:user_type>/classes/<int:class_id>/students/add/',
        TemplateView.as_view(template_name="frontend/add_student_classroom.html"),
        name='add_student_classroom'
    ),
    path(
        'dashboard/<str:user_type>/classes/<int:class_id>/exams/<int:exam_id>/questions/',
        TemplateView.as_view(template_name="frontend/questions.html"),
        name='exam_detail'
    ),
    path(
        "dashboard/<str:user_type>/classes/<int:classroom_id>/exams/<int:exam_id>/add-question/",
        TemplateView.as_view(template_name="frontend/add_question.html"),
        name='exam_detail'
    ),
    path(
        "dashboard/<str:user_type>/classes/<int:classroom_id>/exams/<int:exam_id>/edit/",
        TemplateView.as_view(template_name="frontend/update_exam.html"),
        name='exam_update'
    ),
    path(
        "dashboard/<str:user_type>/classes/<int:classroom_id>/exams/<int:exam_id>/grade/",
        TemplateView.as_view(template_name="frontend/user_answer.html"),
        name='user_answer'
    ),
    path(
        "dashboard/<str:user_type>/classes/<int:classroom_id>/exams/<int:exam_id>/results/",
        TemplateView.as_view(template_name="frontend/student_results.html"),
        name='student_result'
    ),
    path(
        "dashboard/<str:user_type>/classes/<int:classroom_id>/exams/<int:exam_id>/questions/<int:question_id>/edit/",
        TemplateView.as_view(template_name="frontend/edit_questions.html"),
        name='edit_question'
    ),
    path(
        'dashboard/<str:user_type>/teachers/',
        TemplateView.as_view(template_name="frontend/teachers.html"),
        name='teachers'
    ),
    path(
        "dashboard/<str:user_type>/teachers/add/",
        TemplateView.as_view(template_name="frontend/add_teacher.html"),
        name='add_teachers'
    ),
    path(
        'dashboard/<str:user_type>/students/',
        TemplateView.as_view(template_name="frontend/students.html"),
        name='students'
    ),
    path(
        "dashboard/<str:user_type>/students/add/",
        TemplateView.as_view(template_name="frontend/add_student.html"),
        name='add_students'
    ),
    path(
        "dashboard/<str:user_type>/classes/<int:classroom_id>/exams/<int:exam_id>/feedback/",
        TemplateView.as_view(template_name="frontend/feedbacks.html"),
        name='feedbacks'
    ),

]
