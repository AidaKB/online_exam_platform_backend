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

    path('classrooms/<int:classroom_id>/exams/', views.ExamListCreateAPIView.as_view(), name='exam'),
    path('classrooms/<int:classroom_id>/exams/<int:pk>/', views.ExamDetailAPIView.as_view(), name='exam-detail'),

    path('classrooms/<int:classroom_id>/exams/<int:exam_id>/questions/', views.QuestionListCreateAPIView.as_view(),
         name='question'),
    path('classrooms/<int:classroom_id>/exams/<int:exam_id>/questions/<int:pk>/', views.QuestionDetailAPIView.as_view()
         , name='question-detail'),

    path('classrooms/<int:classroom_id>/exams/<int:exam_id>/questions/<int:question_id>/options/'
         , views.OptionListCreateAPIView.as_view(), name='option'),
    path('classrooms/<int:classroom_id>/exams/<int:exam_id>/questions/<int:question_id>/options/<int:pk>'
         , views.OptionDetailAPIView.as_view(), name='option'),

]
