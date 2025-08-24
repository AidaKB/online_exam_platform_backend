from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.serializers import StudentSerializer
from . import models
from core import serializers as core_serializers
from django.utils import timezone as dj_timezone


class ClassroomSerializer(serializers.ModelSerializer):
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
                  "teacher_id",
                  "teacher",)

    def validate(self, attrs):
        user = self.context['request'].user

        if hasattr(user, 'teacher'):
            attrs['teacher'] = user.teacher

        elif hasattr(user, 'institute'):
            teacher = attrs.get('teacher')
            if teacher.institute_id != user.institute.id:
                raise serializers.ValidationError({'teacher_id': 'استاد انتخاب ‌شده متعلق به موسسه شما نیست.'})
        elif getattr(user, "user_type", None) == "admin":
            return attrs
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

        if classroom.teacher.institute != student.institute:
            raise serializers.ValidationError("کلاس و دانش‌آموز باید متعلق به یک موسسه باشند.")

        attrs['classroom'] = classroom
        attrs['student'] = student

        attrs.pop('classroom_id', None)
        attrs.pop('student_id', None)

        return attrs


class MajorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Major
        fields = "__all__"

    def create(self, validated_data):
        user = self.context['request'].user

        if not (hasattr(user, 'institute')) and not (getattr(user, 'user_type', None) == 'admin'):
            raise serializers.ValidationError("شما اجازه افزودن رشته را ندارید.")

        return super().create(validated_data)


class ExamCategorySerializer(serializers.ModelSerializer):
    creator = core_serializers.CustomUserSerializer(read_only=True)

    class Meta:
        model = models.ExamCategory
        fields = "__all__"

    def create(self, validated_data):
        user = self.context['request'].user

        if user.user_type not in ['admin', 'teacher', 'institute']:
            raise serializers.ValidationError("فقط مدیر یا استاد مجاز به ساخت دسته‌بندی هستند.")

        validated_data['creator'] = user
        return super().create(validated_data)


class ExamSerializer(serializers.ModelSerializer):
    classroom = serializers.PrimaryKeyRelatedField(read_only=True)
    creator = core_serializers.CustomUserSerializer(read_only=True)

    class Meta:
        model = models.Exam
        fields = '__all__'

    def validate(self, attrs):
        user = self.context['request'].user

        if not (hasattr(user, 'teacher') or hasattr(user, 'institute') or user.user_type == 'admin'):
            raise serializers.ValidationError("فقط استاد، موسسه یا ادمین می‌توانند آزمون بسازند.")

        start_time = attrs.get('start_time')
        end_time = attrs.get('end_time')
        result_show_time = attrs.get('result_show_time')
        duration_minutes = attrs.get('duration_minutes')

        if start_time >= end_time:
            raise serializers.ValidationError("زمان شروع باید قبل از زمان پایان باشد.")

        if result_show_time < end_time:
            raise serializers.ValidationError("زمان نمایش پاسخ نباید زودتر از زمان اتمام آزمون باشد.")

        total_duration = (end_time - start_time).total_seconds() / 60
        if duration_minutes > total_duration:
            raise serializers.ValidationError("مدت زمان آزمون نمی‌تواند بیشتر از فاصله بین زمان شروع و پایان باشد.")

        return attrs

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        classroom_id = self.context['view'].kwargs.get('classroom_id')

        try:
            classroom = models.Classroom.objects.get(pk=classroom_id)
        except models.Classroom.DoesNotExist:
            raise serializers.ValidationError({"classroom": "کلاس مورد نظر وجود ندارد."})

        if hasattr(user, 'institute'):
            if classroom.teacher.institute_id != user.institute.id:
                raise serializers.ValidationError({"classroom": "این کلاس متعلق به موسسه شما نیست."})

        elif hasattr(user, 'teacher'):
            if classroom.teacher_id != user.teacher.id:
                raise serializers.ValidationError({"classroom": "شما فقط می‌توانید برای کلاس خودتان آزمون بسازید."})

        elif hasattr(user, 'student'):
            raise serializers.ValidationError("شما اجازه ساخت آزمون را ندارید.")

        validated_data['creator'] = user
        validated_data['classroom'] = classroom
        return super().create(validated_data)


class QuestionSerializer(serializers.ModelSerializer):
    exam = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = models.Question
        fields = "__all__"

    def validate(self, attrs):
        user = self.context['request'].user
        exam_id = self.context['view'].kwargs.get('exam_id')
        try:
            exam = models.Exam.objects.get(pk=exam_id)
        except models.Exam.DoesNotExist:
            raise serializers.ValidationError({"exam": "آزمون مشخص‌شده وجود ندارد."})

        if not (user.user_type == 'admin' or hasattr(user, 'teacher') or hasattr(user, 'institute')):
            raise serializers.ValidationError("شما اجازه ایجاد سوال را ندارید.")

        if hasattr(user, 'institute') and exam.classroom.teacher.institute != user.institute:
            raise serializers.ValidationError(
                "شما نمی‌توانید برای این آزمون سوال بسازید، این آزمون متعلق به موسسه شما نیست.")

        if hasattr(user, 'teacher') and exam.classroom.teacher != user.teacher:
            raise serializers.ValidationError("شما فقط می‌توانید برای کلاس خودتان سوال بسازید.")

        attrs['exam'] = exam
        return attrs

    def create(self, validated_data):
        return super().create(validated_data)


class OptionSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = models.Option
        fields = ['id', 'question', 'text', 'is_correct']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        user = request.user if request else None
        instance = kwargs.get('instance')

        if hasattr(user, 'student') and instance:
            exam = instance.question.exam
            now = dj_timezone.now()
            if now < exam.end_time:
                self.fields.pop('is_correct', None)


class UserAnswerSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Student.objects.all(),
        source="user",
        write_only=True,
        required=False
    )
    question_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Question.objects.all(),
        source="question",
        write_only=True
    )

    user = serializers.SerializerMethodField(read_only=True)
    question = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.UserAnswer
        fields = ['id', 'user', 'user_id', 'question', 'question_id', 'answer_text', 'score']

    def get_user(self, obj):
        return StudentSerializer(obj.user).data

    def get_question(self, obj):
        return QuestionSerializer(obj.question).data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context['request'].user
        is_create = self.instance is None

        if hasattr(user, 'student') and is_create:
            self.fields.pop('score')

    def get_fields(self):
        fields = super().get_fields()
        user = self.context['request'].user
        if self.instance and hasattr(user, 'student'):
            fields['score'].read_only = True
        return fields

    def validate(self, attrs):
        user = self.context['request'].user
        question = attrs.get('question') or (self.instance.question if self.instance else None)

        if self.instance is None:
            if hasattr(user, 'student'):
                already_exists = models.UserAnswer.objects.filter(
                    question=question,
                    user=user.student
                ).exists()
                if already_exists:
                    raise serializers.ValidationError("شما قبلاً به این سوال پاسخ داده‌اید.")

            elif user.is_superuser:
                target_user = attrs.get('user')
                if target_user:
                    already_exists = models.UserAnswer.objects.filter(
                        question=question,
                        user=target_user
                    ).exists()
                    if already_exists:
                        raise serializers.ValidationError("این دانش‌آموز قبلاً به این سوال پاسخ داده است.")

        if self.instance and not hasattr(user, 'student'):
            score = attrs.get('score')
            if score is not None and score > self.instance.question.score:
                raise serializers.ValidationError(
                    {"score": f"نمره واردشده نباید بیشتر از {self.instance.question.score} باشد."}
                )

        return attrs

    def update(self, instance, validated_data):
        old_score = instance.score
        new_score = validated_data.get('score', old_score)

        response = super().update(instance, validated_data)

        if old_score != new_score:
            if new_score > self.instance.question.score:
                raise serializers.ValidationError({
                    "score": f"نمره واردشده نمی‌تواند بیشتر از {self.instance.question.score} باشد."
                })

            student = instance.user
            exam = instance.question.exam

            result, created = models.UserExamResult.objects.get_or_create(user=student, exam=exam)

            result.score = result.score - old_score + new_score
            result.save()

        return response


class UserOptionsSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Student.objects.all(),
        source="user",
        write_only=True,
        required=False
    )
    question_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Question.objects.all(),
        source="question",
        write_only=True
    )
    answer_option_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Option.objects.all(),
        source="answer_option",
        write_only=True
    )

    user = serializers.SerializerMethodField(read_only=True)
    question = serializers.SerializerMethodField(read_only=True)
    answer_option = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.UserOptions
        fields = [
            'id',
            'user', 'user_id',
            'question', 'question_id',
            'answer_option', 'answer_option_id'
        ]

    def get_user(self, obj):
        return StudentSerializer(obj.user).data

    def get_question(self, obj):
        return QuestionSerializer(obj.question).data

    def get_answer_option(self, obj):
        return OptionSerializer(obj.answer_option).data

    def validate(self, attrs):
        user = self.context['request'].user
        question = attrs.get('question')

        if question.question_type not in ['MultipleChoice', 'TrueFalse']:
            raise serializers.ValidationError('فقط سوالات تستی قابل پاسخ‌دهی هستند.')

        if hasattr(user, 'student'):
            if question.exam.classroom.teacher.institute != user.student.institute:
                raise serializers.ValidationError('شما اجازه پاسخ به این سوال را ندارید.')
            attrs['user'] = user.student

        elif user.is_superuser:
            if 'user' not in attrs:
                raise serializers.ValidationError('ارسال دانش‌آموز الزامی است.')
        else:
            raise serializers.ValidationError('شما اجازه انجام این عملیات را ندارید.')

        return attrs

    def create(self, validated_data):
        instance = super().create(validated_data)
        self._update_exam_score(instance, None)
        return instance

    def update(self, instance, validated_data):
        old_option = instance.answer_option
        instance = super().update(instance, validated_data)
        self._update_exam_score(instance, old_option)
        return instance

    def _update_exam_score(self, instance, old_option):
        student = instance.user
        exam = instance.question.exam
        question_score = instance.question.score
        new_option = instance.answer_option

        exam_result, created = models.UserExamResult.objects.get_or_create(
            user=student, exam=exam,
            defaults={'score': 0}
        )

        old_correct = old_option.is_correct if old_option else False
        new_correct = new_option.is_correct

        if not old_correct and new_correct:
            exam_result.score += question_score
            exam_result.save()

        elif old_correct and not new_correct:
            exam_result.score -= question_score
            exam_result.save()


class UserExamResultSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Student.objects.all(),
        source="user",
        write_only=True,
        required=False
    )
    exam_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Exam.objects.all(),
        source="exam",
        write_only=True,
        required=False
    )
    user = serializers.SerializerMethodField(read_only=True)
    exam = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.UserExamResult
        fields = ['id', 'user', 'user_id', 'exam', 'exam_id', 'score']

    def get_user(self, obj):
        return StudentSerializer(obj.user).data

    def get_exam(self, obj):
        return ExamSerializer(obj.exam).data


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Feedback
        fields = '__all__'
        read_only_fields = ['user']

    def create(self, validated_data):
        user = self.context['request'].user
        if hasattr(user, 'student'):
            validated_data['user'] = user.student
        return super().create(validated_data)
