from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from . import models
from . import serializers
from . import permissions
from . import filters
from .models import Major


class ClassroomListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.ClassroomSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.ClassroomFilter

    search_fields = [
        'name',
        'grade',
        'teacher__account__first_name',
        'teacher__account__last_name',
        'teacher__phone_number',
        'teacher__institute__name',
    ]

    ordering_fields = [
        'name',
        'grade',
        'teacher__account__first_name',
        'teacher__account__last_name',
        'teacher__phone_number',
        'teacher__institute__name',
    ]

    ordering = ['name']

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "student"):
            return models.Classroom.objects.filter(student_classroom__student=user.student)
        elif hasattr(user, "teacher"):
            return models.Classroom.objects.filter(teacher=user.teacher)
        elif hasattr(user, "institute"):
            return models.Classroom.objects.filter(teacher__institute=user.institute)
        else:
            return models.Classroom.objects.all()

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), permissions.IsTeacherOrInstituteOrAdmin()]
        return [IsAuthenticated()]


class ClassroomDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Classroom.objects.all()
    serializer_class = serializers.ClassroomSerializer
    permission_classes = [IsAuthenticated, permissions.IsAdminOrTeacherOrInstituteOwner]


class StudentClassroomListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.StudentClassroomSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.StudentClassroomFilter
    search_fields = [
        'classroom__name',
        'classroom__grade',
        'classroom__teacher__account__first_name',
        'classroom__teacher__account__last_name',
        'student__account__first_name',
        'student__account__last_name',
    ]
    ordering_fields = [
        'classroom__name',
        'classroom__grade',
        'classroom__teacher__account__first_name',
        'classroom__teacher__account__last_name',
        'student__account__first_name',
        'student__account__last_name',
    ]
    ordering = ['classroom__name']  # پیش‌فرض

    def get_queryset(self):
        user = self.request.user

        if getattr(user, 'user_type', None) == 'admin':
            return models.StudentClassroom.objects.all()

        elif hasattr(user, 'institute'):
            return models.StudentClassroom.objects.filter(classroom__institute=user.institute)

        elif hasattr(user, 'teacher'):
            return models.StudentClassroom.objects.filter(classroom__teacher=user.teacher)

        elif hasattr(user, 'student'):
            return models.StudentClassroom.objects.filter(student=user.student)

        return models.StudentClassroom.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        classroom = serializer.validated_data['classroom']

        if getattr(user, 'user_type', None) == 'admin':
            serializer.save()

        elif hasattr(user, 'institute') and classroom.teacher.institute == user.institute:
            serializer.save()

        elif hasattr(user, 'teacher') and classroom.teacher == user.teacher:
            serializer.save()

        else:
            raise PermissionDenied("شما اجازه افزودن دانش‌آموز به این کلاس را ندارید.")


class StudentClassroomDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.StudentClassroomSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        obj = get_object_or_404(models.StudentClassroom, pk=self.kwargs["pk"])

        if getattr(user, 'user_type', None) == 'admin':
            return obj

        if hasattr(user, 'student'):
            if self.request.method == 'GET' and obj.student_id == user.student.id:
                return obj
            raise PermissionDenied("دانش‌آموز فقط می‌تواند پاسخ‌های خودش را مشاهده کند.")

        if hasattr(user, 'institute'):
            if obj.classroom.teacher.institute_id == user.institute.id:
                return obj
            raise PermissionDenied("این کلاس متعلق به موسسه شما نیست.")

        if hasattr(user, 'teacher'):
            if obj.classroom.teacher_id == user.teacher.id:
                return obj
            raise PermissionDenied("شما استاد این کلاس نیستید.")

        raise PermissionDenied("شما مجاز به انجام این عملیات نیستید.")


class MajorListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.MajorSerializer
    permission_classes = [IsAuthenticated]
    queryset = Major.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.MajorFilter

    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']


class MajorDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Major.objects.all()
    serializer_class = serializers.MajorSerializer
    permission_classes = [IsAdminUser]


class ExamCategoryListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.ExamCategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.ExamCategoryFilter
    search_fields = [
        'name',
        'creator__first_name',
        'creator__last_name',
        'creator__username',
        'creator__user_type',
    ]
    ordering_fields = [
        'name',
        'creator__first_name',
        'creator__last_name',
        'creator__username',
        'creator__user_type',
    ]
    ordering = ['name']

    def get_queryset(self):
        user = self.request.user

        if user.user_type == 'admin':
            return models.ExamCategory.objects.all()

        elif hasattr(user, 'teacher'):
            return models.ExamCategory.objects.filter(
                Q(creator=user) | Q(creator__user_type='admin')
            )

        return models.ExamCategory.objects.none()

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), permissions.IsAdminOrTeacher()]
        return [IsAuthenticated()]


class ExamCategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.ExamCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'admin':
            return models.ExamCategory.objects.all()
        elif hasattr(user, 'teacher'):
            return models.ExamCategory.objects.filter(
                Q(creator=user) | Q(creator__user_type='admin')
            )
        return models.ExamCategory.objects.none()

    def perform_update(self, serializer):
        user = self.request.user
        instance = self.get_object()

        if user.user_type == 'admin' or instance.creator == user:
            serializer.save()
        else:
            raise PermissionDenied("شما مجاز به ویرایش این دسته‌بندی نیستید.")

    def perform_destroy(self, instance):
        user = self.request.user

        if user.user_type == 'admin' or instance.creator == user:
            instance.delete()
        else:
            raise PermissionDenied("شما مجاز به حذف این دسته‌بندی نیستید.")


class ExamListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.ExamSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.ExamFilter

    search_fields = [
        'title',
        'description',
        'category__name',
        'creator__first_name',
        'creator__last_name',
        'classroom__name',
    ]

    ordering_fields = [
        'title',
        'start_time',
        'end_time',
        'duration_minutes',
        'status',
        'category__name',
        'creator__first_name',
        'creator__last_name',
        'classroom__name',
    ]

    ordering = ['start_time']

    def get_queryset(self):
        user = self.request.user
        classroom_id = self.kwargs.get('classroom_id')  # گرفتن classroom_id از URL

        base_qs = models.Exam.objects.filter(classroom_id=classroom_id)

        if user.user_type == 'admin':
            return base_qs

        elif hasattr(user, 'institute'):
            return base_qs.filter(
                classroom__teacher__institute=user.institute
            )

        elif hasattr(user, 'teacher'):
            return base_qs.filter(
                classroom__teacher=user.teacher
            )

        elif hasattr(user, 'student'):
            return base_qs.filter(
                classroom__teacher__institute=user.student.institute
            ).distinct()

        return models.Exam.objects.none()

    def perform_create(self, serializer):
        serializer.save()


class ExamDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Exam.objects.all()
    serializer_class = serializers.ExamSerializer
    permission_classes = [IsAuthenticated, permissions.IsAdminOrInstituteOrCreatorTeacher]


class QuestionListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.QuestionSerializer
    permission_classes = [IsAuthenticated, permissions.IsAdminOrInstituteOrTeacherForQuestion]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.QuestionFilter

    search_fields = [
        'text',
        'question_type',
        'exam__title',
        'exam__description',
        'exam__classroom__name',
        'exam__classroom__grade',
        'exam__category__name',
        'exam__creator__first_name',
        'exam__creator__last_name',
    ]

    ordering_fields = [
        'text',
        'question_type',
        'score',
        'exam__title',
        'exam__start_time',
        'exam__end_time',
        'exam__classroom__name',
        'exam__creator__first_name',
        'exam__creator__last_name',
    ]

    ordering = ['exam__start_time']

    def get_queryset(self):
        user = self.request.user

        if user.user_type == 'admin':
            return models.Question.objects.all()

        if hasattr(user, 'institute'):
            return models.Question.objects.filter(
                exam__classroom__teacher__institute=user.institute
            )

        if hasattr(user, 'teacher'):
            return models.Question.objects.filter(
                exam__classroom__teacher=user.teacher
            )

        if hasattr(user, 'student'):
            return models.Question.objects.filter(
                exam__classroom__teacher__institute=user.student.institute
            ).distinct()

        return models.Question.objects.none()


class QuestionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.QuestionSerializer
    permission_classes = [IsAuthenticated, permissions.IsAdminOrInstituteOrTeacherForQuestion]

    def get_queryset(self):
        return models.Question.objects.select_related('exam__classroom__teacher__institute')


class OptionListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.OptionSerializer
    permission_classes = [IsAuthenticated, permissions.OptionPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.OptionFilter

    search_fields = [
        'text',
        'question__text',
        'question__exam__title',
    ]

    ordering_fields = [
        'text',
        'is_correct',
        'question__text',
        'question__exam__title',
    ]

    ordering = ['text']

    def get_queryset(self):
        user = self.request.user
        question_id = self.kwargs.get('question_id')
        queryset = models.Option.objects.filter(question_id=question_id)

        if user.is_superuser:
            return queryset

        elif hasattr(user, 'teacher'):
            return queryset.filter(question__exam__classroom__teacher=user.teacher)

        elif hasattr(user, 'institute'):
            return queryset.filter(question__exam__classroom__teacher__institute=user.institute)

        elif hasattr(user, 'student'):
            return queryset.filter(question__exam__classroom__teacher__institute=user.student.institute)

        return models.Option.objects.none()

    def perform_create(self, serializer):
        question_id = self.kwargs.get('question_id')
        try:
            question = models.Question.objects.get(pk=question_id)
        except models.Question.DoesNotExist:
            raise serializers.ValidationError({"question": "سوال مشخص‌شده وجود ندارد."})

        serializer.save(question=question)


class OptionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.OptionSerializer
    permission_classes = [IsAuthenticated, permissions.OptionPermission]

    def get_queryset(self):
        user = self.request.user
        queryset = models.Option.objects.filter(
            question_id=self.kwargs.get('question_id')
        ).select_related('question__exam__classroom__teacher__institute')

        if user.is_superuser:
            return queryset

        elif hasattr(user, 'institute'):
            return queryset.filter(question__exam__classroom__teacher__institute=user.institute)

        elif hasattr(user, 'teacher'):
            return queryset.filter(question__exam__classroom__teacher=user.teacher)

        elif hasattr(user, 'student'):
            return queryset.filter(question__exam__classroom__teacher__institute=user.student.institute)

        return models.Option.objects.none()


class UserAnswerListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.UserAnswer.objects.select_related(
        'question__exam__classroom__teacher__institute', 'user'
    )
    serializer_class = serializers.UserAnswerSerializer
    permission_classes = [permissions.UserAnswerPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.UserAnswerFilter

    search_fields = [
        'answer_text',
        'user__account__first_name',
        'user__account__last_name',
        'user__national_code',
        'question__text',
        'question__exam__title',
        'question__exam__classroom__name',
        'question__exam__classroom__teacher__institute__name',
    ]

    ordering_fields = [
        'score',
        'user__account__first_name',
        'user__account__last_name',
        'question__text',
        'question__exam__title',
    ]

    ordering = ['-score']

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return models.UserAnswer.objects.all()

        if hasattr(user, 'institute'):
            return models.UserAnswer.objects.filter(
                question__exam__classroom__teacher__institute=user.institute)

        if hasattr(user, 'teacher'):
            return models.UserAnswer.objects.filter(
                question__exam__classroom__teacher=user.teacher)

        if hasattr(user, 'student'):
            return models.UserAnswer.objects.filter(user=user.student)

        return models.UserAnswer.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        question = serializer.validated_data['question']

        if question.question_type != 'Descriptive':
            raise ValidationError("فقط برای سوالات تشریحی می‌توانید پاسخ ثبت کنید.")

        if hasattr(user, 'student'):
            if question.exam.classroom.teacher.institute != user.student.institute:
                raise ValidationError("شما مجاز به پاسخ به این سوال نیستید.")
            serializer.save(user=user.student)

        elif user.is_superuser:
            if 'user' not in serializer.validated_data:
                raise ValidationError("ادمین باید دانش‌آموز را مشخص کند.")
            serializer.save()

        else:
            raise ValidationError("فقط دانش‌آموز یا ادمین می‌توانند پاسخ ثبت کنند.")


class UserAnswerDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.UserAnswer.objects.select_related(
        'question__exam__classroom__teacher__institute', 'user'
    )
    serializer_class = serializers.UserAnswerSerializer
    permission_classes = [permissions.UserAnswerPermission]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return models.UserAnswer.objects.all()

        if hasattr(user, 'institute'):
            return models.UserAnswer.objects.filter(
                question__exam__classroom__teacher__institute=user.institute)

        if hasattr(user, 'teacher'):
            return models.UserAnswer.objects.filter(
                question__exam__classroom__teacher=user.teacher)

        if hasattr(user, 'student'):
            return models.UserAnswer.objects.filter(user=user.student)

        return models.UserAnswer.objects.none()


class UserOptionsListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.UserOptionsSerializer
    permission_classes = [IsAuthenticated, permissions.UserOptionsPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.UserOptionsFilter

    search_fields = [
        'user__account__first_name',
        'user__account__last_name',
        'user__national_code',
        'question__text',
        'question__exam__title',
        'question__exam__classroom__name',
        'answer_option__text',
    ]

    ordering_fields = [
        'user__account__first_name',
        'user__account__last_name',
        'question__text',
        'answer_option__text',
        'question__exam__title',
    ]

    ordering = ['user__account__last_name']

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return models.UserOptions.objects.all()

        elif hasattr(user, 'institute'):
            return models.UserOptions.objects.filter(
                question__exam__classroom__teacher__institute=user.institute
            )

        elif hasattr(user, 'teacher'):
            return models.UserOptions.objects.filter(
                question__exam__classroom__teacher=user.teacher
            )

        elif hasattr(user, 'student'):
            return models.UserOptions.objects.filter(user=user.student)

        return models.UserOptions.objects.none()


class UserOptionsDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.UserOptionsSerializer
    permission_classes = [IsAuthenticated, permissions.UserOptionsPermission]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return models.UserOptions.objects.all()

        elif hasattr(user, 'institute'):
            return models.UserOptions.objects.filter(
                question__exam__classroom__teacher__institute=user.institute
            )

        elif hasattr(user, 'teacher'):
            return models.UserOptions.objects.filter(
                question__exam__classroom__teacher=user.teacher
            )

        elif hasattr(user, 'student'):
            return models.UserOptions.objects.filter(user=user.student)

        return models.UserOptions.objects.none()


class UserExamResultListAPIView(generics.ListAPIView):
    serializer_class = serializers.UserExamResultSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user', 'exam', 'score', 'exam__classroom', 'exam__classroom__teacher',
                        'exam__result_show_time']

    search_fields = [
        'user__account__first_name', 'user__account__last_name', 'user__account__username',
        'exam__title', 'exam__classroom__name',
        'exam__classroom__teacher__account__first_name',
        'exam__classroom__teacher__account__last_name'
    ]

    ordering_fields = ['score', 'exam__result_show_time', 'exam__title', 'user', 'exam']

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return models.UserExamResult.objects.all()

        elif hasattr(user, 'institute'):
            return models.UserExamResult.objects.filter(
                exam__classroom__teacher__institute=user.institute
            )

        elif hasattr(user, 'teacher'):
            return models.UserExamResult.objects.filter(
                exam__classroom__teacher=user.teacher
            )


        elif hasattr(user, 'student'):
            now = timezone.now()

            return models.UserExamResult.objects.filter(
                user=user.student
            ).filter(

                Q(exam__result_show_time__lte=now) | Q(exam__result_show_time__isnull=True)
            )
        return models.UserExamResult.objects.none()


class UserExamResultDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.UserExamResult.objects.select_related('exam__classroom__teacher', 'user')
    serializer_class = serializers.UserExamResultSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        user = self.request.user

        if user.is_superuser:
            return obj

        if hasattr(user, 'institute'):
            if obj.exam.classroom.teacher.institute == user.institute:
                return obj
            raise PermissionDenied("شما به این نتیجه دسترسی ندارید.")

        if hasattr(user, 'teacher'):
            if obj.exam.classroom.teacher == user.teacher:
                return obj
            raise PermissionDenied("شما به این نتیجه دسترسی ندارید.")

        if hasattr(user, 'student'):
            if obj.user == user.student:
                now = timezone.now()
                if obj.exam.result_show_time is None or obj.exam.result_show_time <= now:
                    if self.request.method in ['PUT', 'PATCH', 'DELETE']:
                        raise PermissionDenied("شما اجازه ویرایش یا حذف این نتیجه را ندارید.")
                    return obj
                raise PermissionDenied("هنوز زمان مشاهده نتیجه این آزمون فرا نرسیده است.")

        raise PermissionDenied("شما اجازه دسترسی به این نتیجه را ندارید.")


class FeedbackListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.FeedbackSerializer
    permission_classes = [IsAuthenticated, permissions.FeedbackPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.FeedbackFilter

    search_fields = [
        'user__account__first_name',
        'user__account__last_name',
        'user__national_code',
        'exam__title',
        'exam__classroom__name',
        'text',
    ]

    ordering_fields = [
        'user__account__first_name',
        'user__account__last_name',
        'exam__title',
    ]

    ordering = ['user__account__last_name']

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return models.Feedback.objects.all()

        if hasattr(user, 'institute'):
            return models.Feedback.objects.filter(exam__classroom__teacher__institute=user.institute)

        if hasattr(user, 'teacher'):
            return models.Feedback.objects.filter(exam__classroom__teacher=user.teacher)

        if hasattr(user, 'student'):
            return models.Feedback.objects.filter(user=user.student)

        return models.Feedback.objects.none()


class FeedbackDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.FeedbackSerializer
    permission_classes = [IsAuthenticated, permissions.FeedbackPermission]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return models.Feedback.objects.all()

        if hasattr(user, 'institute'):
            return models.Feedback.objects.filter(exam__classroom__teacher__institute=user.institute)

        if hasattr(user, 'teacher'):
            return models.Feedback.objects.filter(exam__classroom__teacher=user.teacher)

        if hasattr(user, 'student'):
            return models.Feedback.objects.filter(user=user.student)

        return models.Feedback.objects.none()
