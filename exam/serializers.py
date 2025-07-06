from rest_framework import serializers
from . import models
from core import serializers as core_serializers


class ClassroomSerializer(serializers.ModelSerializer):
    institute_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Institute.objects.all(),
        source='institute',
        write_only=True,
        error_messages={
            'does_not_exist': 'شناسه موسسه معتبر نیست.',
            'incorrect_type': 'شناسه موسسه باید عدد باشد.',
        }
    )
    institute = core_serializers.InstituteSerializer(read_only=True)

    teacher_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Teacher.objects.all(),
        source='teacher',
        write_only=True,
        error_messages={
            'does_not_exist': 'شناسه استاد معتبر نیست.',
            'incorrect_type': 'شناسه استاد باید عدد باشد.',
        }
    )
    teacher = core_serializers.TeacherSerializer(read_only=True)

    class Meta:
        model = models.Classroom
        fields = ("id",
                  "name",
                  "grade",
                  "description",
                  "created_at",
                  "institute_id",
                  "institute",
                  "teacher_id",
                  "teacher",)

    def validate(self, attrs):
        user = self.context['request'].user

        if hasattr(user, 'teacher'):
            attrs['institute'] = user.teacher.institute
            attrs['teacher'] = user.teacher

        elif hasattr(user, 'institute'):
            teacher = attrs.get('teacher')
            if teacher.institute_id != user.institute.id:
                raise serializers.ValidationError({'teacher_id': 'استاد انتخاب‌شده متعلق به موسسه شما نیست.'})
            attrs['institute'] = user.institute

        elif getattr(user, 'user_type', None) == 'admin':
            teacher = attrs.get('teacher')
            institute = attrs.get('institute')
            if teacher.institute_id != institute.id:
                raise serializers.ValidationError({'teacher_id': 'استاد متعلق به موسسه مشخص‌شده نیست.'})

        else:
            raise serializers.ValidationError("فقط استاد، موسسه یا مدیر سامانه مجاز به ساخت کلاس هستند.")

        return attrs


class StudentClassroomSerializer(serializers.ModelSerializer):
    classroom_id = serializers.IntegerField(write_only=True)
    classroom = serializers.StringRelatedField(read_only=True)

    student_id = serializers.IntegerField(write_only=True)
    student = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = models.StudentClassroom
        fields = [
            'id',
            'classroom_id',
            'classroom',
            'student_id',
            'student',
        ]

    def validate(self, attrs):
        user = self.context['request'].user

        if hasattr(user, 'student'):
            raise serializers.ValidationError("دانش‌آموزان اجازه افزودن به کلاس را ندارند.")

        try:
            classroom = models.Classroom.objects.get(id=attrs['classroom_id'])
        except models.Classroom.DoesNotExist:
            raise serializers.ValidationError({'classroom_id': 'کلاس موردنظر یافت نشد.'})

        try:
            student = models.Student.objects.get(id=attrs['student_id'])
        except models.Student.DoesNotExist:
            raise serializers.ValidationError({'student_id': 'دانش‌آموز یافت نشد.'})

        if classroom.institute != student.institute:
            raise serializers.ValidationError("کلاس و دانش‌آموز باید متعلق به یک موسسه باشند.")

        attrs['classroom'] = classroom
        attrs['student'] = student

        attrs.pop('classroom_id', None)
        attrs.pop('student_id', None)

        return attrs
