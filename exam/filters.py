# filters.py
import django_filters
from . import models


class ClassroomFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    grade = django_filters.CharFilter(lookup_expr='icontains')
    teacher_name = django_filters.CharFilter(field_name='teacher__account__first_name', lookup_expr='icontains')
    teacher_last_name = django_filters.CharFilter(field_name='teacher__account__last_name', lookup_expr='icontains')
    teacher_phone_number = django_filters.CharFilter(field_name='teacher__phone_number', lookup_expr='icontains')
    institute_name = django_filters.CharFilter(field_name='teacher__institute__name', lookup_expr='icontains')

    class Meta:
        model = models.Classroom
        fields = [
            'name',
            'grade',
            'teacher',
            'teacher_name',
            'teacher_last_name',
            'teacher_phone_number',
            'teacher__institute',
            'institute_name',
        ]


class StudentClassroomFilter(django_filters.FilterSet):
    classroom_name = django_filters.CharFilter(field_name='classroom__name', lookup_expr='icontains')
    classroom_grade = django_filters.CharFilter(field_name='classroom__grade', lookup_expr='icontains')
    teacher_name = django_filters.CharFilter(field_name='classroom__teacher__account__first_name',
                                             lookup_expr='icontains')
    teacher_last_name = django_filters.CharFilter(field_name='classroom__teacher__account__last_name',
                                                  lookup_expr='icontains')
    student_name = django_filters.CharFilter(field_name='student__account__first_name', lookup_expr='icontains')
    student_last_name = django_filters.CharFilter(field_name='student__account__first_name', lookup_expr='icontains')

    class Meta:
        model = models.StudentClassroom
        fields = [
            'classroom',
            'student',
            'classroom_name',
            'classroom_grade',
            'teacher_name',
            'teacher_last_name',
            'student_name',
            'student_last_name'
        ]


class MajorFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = models.Major
        fields = ['name']


class ExamCategoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    creator_first_name = django_filters.CharFilter(field_name='creator__first_name', lookup_expr='icontains')
    creator_last_name = django_filters.CharFilter(field_name='creator__last_name', lookup_expr='icontains')
    creator_username = django_filters.CharFilter(field_name='creator__username', lookup_expr='icontains')
    creator_user_type = django_filters.CharFilter(field_name='creator__user_type', lookup_expr='icontains')

    class Meta:
        model = models.ExamCategory
        fields = [
            'name',
            'creator',
            'creator_first_name',
            'creator_last_name',
            'creator_username',
            'creator_user_type',
        ]


class ExamFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    start_time = django_filters.IsoDateTimeFilter()
    end_time = django_filters.IsoDateTimeFilter()
    status = django_filters.BooleanFilter()
    duration_minutes = django_filters.NumberFilter()
    category_name = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')
    creator_first_name = django_filters.CharFilter(field_name='creator__first_name', lookup_expr='icontains')
    creator_last_name = django_filters.CharFilter(field_name='creator__last_name', lookup_expr='icontains')
    classroom_name = django_filters.CharFilter(field_name='classroom__name', lookup_expr='icontains')

    class Meta:
        model = models.Exam
        fields = [
            'title',
            'description',
            'start_time',
            'end_time',
            'status',
            'duration_minutes',
            'category',
            'category_name',
            'creator',
            'creator_first_name',
            'creator_last_name',
            'classroom',
            'classroom_name',
        ]


class QuestionFilter(django_filters.FilterSet):
    text = django_filters.CharFilter(lookup_expr='icontains')
    question_type = django_filters.CharFilter(lookup_expr='icontains')
    score = django_filters.NumberFilter()

    exam_title = django_filters.CharFilter(field_name='exam__title', lookup_expr='icontains')
    exam_description = django_filters.CharFilter(field_name='exam__description', lookup_expr='icontains')
    exam_classroom_name = django_filters.CharFilter(field_name='exam__classroom__name', lookup_expr='icontains')
    exam_category_name = django_filters.CharFilter(field_name='exam__category__name', lookup_expr='icontains')
    exam_creator_first_name = django_filters.CharFilter(field_name='exam__creator__first_name', lookup_expr='icontains')
    exam_creator_last_name = django_filters.CharFilter(field_name='exam__creator__last_name', lookup_expr='icontains')

    class Meta:
        model = models.Question
        fields = [
            'text',
            'question_type',
            'score',
            'exam',
            'exam_title',
            'exam_description',
            'exam_classroom_name',
            'exam_category_name',
            'exam_creator_first_name',
            'exam_creator_last_name',
        ]


class OptionFilter(django_filters.FilterSet):
    text = django_filters.CharFilter(lookup_expr='icontains')
    is_correct = django_filters.BooleanFilter()
    question_text = django_filters.CharFilter(field_name='question__text', lookup_expr='icontains')
    exam_id = django_filters.NumberFilter(field_name='question__exam__id')

    class Meta:
        model = models.Option
        fields = [
            'text',
            'is_correct',
            'question',
            'question_text',
            'exam_id',
        ]


class UserAnswerFilter(django_filters.FilterSet):
    answer_text = django_filters.CharFilter(lookup_expr='icontains')
    score = django_filters.NumberFilter()
    score__gte = django_filters.NumberFilter(field_name='score', lookup_expr='gte')
    score__lte = django_filters.NumberFilter(field_name='score', lookup_expr='lte')

    student_first_name = django_filters.CharFilter(field_name='user__account__first_name', lookup_expr='icontains')
    student_last_name = django_filters.CharFilter(field_name='user__account__last_name', lookup_expr='icontains')
    student_national_code = django_filters.CharFilter(field_name='user__national_code', lookup_expr='icontains')

    question_text = django_filters.CharFilter(field_name='question__text', lookup_expr='icontains')
    exam_title = django_filters.CharFilter(field_name='question__exam__title', lookup_expr='icontains')
    classroom_name = django_filters.CharFilter(field_name='question__exam__classroom__name', lookup_expr='icontains')
    institute_name = django_filters.CharFilter(field_name='question__exam__classroom__teacher__institute__name',
                                               lookup_expr='icontains')

    class Meta:
        model = models.UserAnswer
        fields = [
            'score',
            'answer_text',
            'user',
            'question',
            'score__gte',
            'score__lte',
            'student_first_name',
            'student_last_name',
            'student_national_code',
            'question_text',
            'exam_title',
            'classroom_name',
            'institute_name',
        ]


class UserOptionsFilter(django_filters.FilterSet):
    student_first_name = django_filters.CharFilter(field_name='user__account__first_name', lookup_expr='icontains')
    student_last_name = django_filters.CharFilter(field_name='user__account__last_name', lookup_expr='icontains')
    student_national_code = django_filters.CharFilter(field_name='user__national_code', lookup_expr='icontains')

    question_text = django_filters.CharFilter(field_name='question__text', lookup_expr='icontains')
    exam_title = django_filters.CharFilter(field_name='question__exam__title', lookup_expr='icontains')
    classroom_name = django_filters.CharFilter(field_name='question__exam__classroom__name', lookup_expr='icontains')

    option_text = django_filters.CharFilter(field_name='answer_option__text', lookup_expr='icontains')

    class Meta:
        model = models.UserOptions
        fields = [
            'user', 'question', 'answer_option',
            'student_first_name', 'student_last_name', 'student_national_code',
            'question_text', 'exam_title', 'classroom_name', 'option_text',
        ]


class FeedbackFilter(django_filters.FilterSet):
    student_first_name = django_filters.CharFilter(field_name='user__account__first_name', lookup_expr='icontains')
    student_last_name = django_filters.CharFilter(field_name='user__account__last_name', lookup_expr='icontains')
    student_national_code = django_filters.CharFilter(field_name='user__national_code', lookup_expr='icontains')
    exam_title = django_filters.CharFilter(field_name='exam__title', lookup_expr='icontains')
    classroom_name = django_filters.CharFilter(field_name='exam__classroom__name', lookup_expr='icontains')

    class Meta:
        model = models.Feedback
        fields = [
            'user', 'exam',
            'student_first_name', 'student_last_name', 'student_national_code',
            'exam_title', 'classroom_name'
        ]
