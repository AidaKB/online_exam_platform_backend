import django_filters
from exam import models


class InstituteFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    registration_code = django_filters.CharFilter(lookup_expr='icontains')
    phone = django_filters.CharFilter(lookup_expr='icontains')
    created_at = django_filters.DateFromToRangeFilter()

    class Meta:
        model = models.Institute
        fields = ['name', 'registration_code', 'phone', 'created_at']


class TeacherFilter(django_filters.FilterSet):
    national_code = django_filters.CharFilter(lookup_expr='icontains')
    phone_number = django_filters.CharFilter(lookup_expr='icontains')
    expertise = django_filters.CharFilter(lookup_expr='icontains')
    created_at = django_filters.DateFromToRangeFilter()

    class Meta:
        model = models.Teacher
        fields = ['national_code', 'phone_number', 'expertise', 'created_at']


class StudentFilter(django_filters.FilterSet):
    national_code = django_filters.CharFilter(lookup_expr='icontains')
    phone_number = django_filters.CharFilter(lookup_expr='icontains')
    gender = django_filters.CharFilter()
    date_of_birth = django_filters.DateFromToRangeFilter()
    created_at = django_filters.DateFromToRangeFilter()

    class Meta:
        model = models.Student
        fields = ['national_code', 'phone_number', 'gender', 'major', 'date_of_birth', 'created_at']
