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
