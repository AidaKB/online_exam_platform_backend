from rest_framework import serializers
from . import models
from core import serializers as core_serializers


class ClassroomSerializer(serializers.ModelSerializer):
    institute_id = serializers.IntegerField(write_only=True)
    institute = core_serializers.InstituteSerializer(read_only=True)

    teacher_id = serializers.IntegerField(write_only=True)
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

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        if hasattr(user, 'teacher'):
            validated_data['institute'] = user.teacher.institute
            validated_data['teacher'] = user.teacher

        elif hasattr(user, 'institute'):
            validated_data['institute'] = user.institute

            teacher_id = validated_data.pop('teacher_id', None)
            if not teacher_id:
                raise serializers.ValidationError({"teacher_id": "ارسال شناسه استاد الزامی است."})

            try:
                teacher = models.Teacher.objects.get(id=teacher_id, institute=user.institute)
            except models.Teacher.DoesNotExist:
                raise serializers.ValidationError({"teacher_id": "استاد یافت نشد یا متعلق به این موسسه نیست."})

            validated_data['teacher'] = teacher

        elif getattr(user, 'user_type', None) == 'admin':
            institute_id = validated_data.pop('institute_id', None)
            teacher_id = validated_data.pop('teacher_id', None)

            if not institute_id:
                raise serializers.ValidationError({"institute_id": "ارسال شناسه موسسه الزامی است."})
            if not teacher_id:
                raise serializers.ValidationError({"teacher_id": "ارسال شناسه استاد الزامی است."})

            try:
                institute = models.Institute.objects.get(id=institute_id)
            except models.Institute.DoesNotExist:
                raise serializers.ValidationError({"institute_id": "موسسه یافت نشد."})

            try:
                teacher = models.Teacher.objects.get(id=teacher_id, institute=institute)
            except models.Teacher.DoesNotExist:
                raise serializers.ValidationError({"teacher_id": "استاد یافت نشد یا متعلق به موسسه مشخص‌شده نیست."})

            validated_data['institute'] = institute
            validated_data['teacher'] = teacher

        else:
            raise serializers.ValidationError("فقط استاد، موسسه یا مدیر سامانه مجاز به ساخت کلاس هستند.")

        return super().create(validated_data)
