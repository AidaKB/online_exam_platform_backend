from django.urls import path
from exam import views

urlpatterns = [
    path('classrooms/', views.ClassroomListCreateAPIView.as_view(), name='classroom'),
    path('classrooms/<int:pk>/', views.ClassroomRetrieveUpdateDeleteAPIView.as_view(), name='classroom-detail'),

    path('students-classrooms/', views.StudentClassroomListCreateAPIView.as_view(), name='students-classroom'),
    path('students-classrooms/<int:pk>/', views.StudentClassroomRetrieveUpdateDeleteAPIView.as_view()
         , name='students-classroom-detail'),

]
