from django.urls import path
from exam import views

urlpatterns = [
    path('classrooms/', views.ClassroomListCreateAPIView.as_view(), name='classroom'),
    path('classrooms/<int:pk>/', views.ClassroomDetailAPIView.as_view(), name='classroom-detail'),

    path('students-classrooms/', views.StudentClassroomListCreateAPIView.as_view(), name='students-classroom'),
    path('students-classrooms/<int:pk>/', views.StudentClassroomDetailAPIView.as_view()
         , name='students-classroom-detail'),

    path('majors/', views.MajorListCreateAPIView.as_view(), name='major'),
    path('majors/<int:pk>/', views.MajorDetailAPIView.as_view(), name='major-detail'),

    path('exam-categories/', views.ExamCategoryListCreateAPIView.as_view(), name='exam-category'),
    path('exam-categories/<int:pk>/', views.ExamCategoryDetailAPIView.as_view(), name='exam-category-detail'),

    path('exams/', views.ExamListCreateAPIView.as_view(), name='exam'),
    path('exams/<int:pk>/', views.ExamDetailAPIView.as_view(), name='exam-detail'),

    path('questions/', views.QuestionListCreateAPIView.as_view(), name='question'),
    path('questions/<int:pk>/', views.QuestionDetailAPIView.as_view(), name='question-detail'),

]
