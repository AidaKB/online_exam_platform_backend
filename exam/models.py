from django.db import models
from core.models import Student, Teacher, Institute, CustomUser
from . import consts


class Classroom(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام کلاس")
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, null=True, blank=True, related_name="classrooms",
                                verbose_name="استاد")
    grade = models.CharField(max_length=30, choices=consts.GRADE_CHOICES, verbose_name="پایه تحصیلی")
    description = models.TextField(null=True, blank=True, verbose_name="توضیحات")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        verbose_name = "کلاس"
        verbose_name_plural = "کلاس‌ها"

    def __str__(self):
        return f"{self.name} - {self.grade}"


class StudentClassroom(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.PROTECT, related_name="student_classroom",
                                  verbose_name="کلاس")
    student = models.ForeignKey(Student, on_delete=models.PROTECT, related_name="student_classroom",
                                verbose_name="دانشجو")


class Major(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام رشته تحصیلی")

    def __str__(self):
        return self.name


class ExamCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام دسته‌بندی")
    creator = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name="exam_categories")

    class Meta:
        verbose_name = "دسته‌بندی آزمون"
        verbose_name_plural = "دسته‌بندی‌های آزمون"

    def __str__(self):
        return self.name


class Exam(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان آزمون")
    description = models.TextField(max_length=500, verbose_name="توضیحات آزمون")
    start_time = models.DateTimeField(verbose_name="زمان شروع")
    end_time = models.DateTimeField(verbose_name="زمان پایان")
    duration_minutes = models.PositiveIntegerField(verbose_name="مدت زمان (دقیقه)")
    status = models.BooleanField(default=True, verbose_name="فعال/غیرفعال")
    category = models.ForeignKey(ExamCategory, on_delete=models.SET_NULL, null=True, verbose_name="دسته‌بندی")
    creator = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="سازنده آزمون")
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name="exams",
                                  verbose_name="کلاس مرتبط")

    class Meta:
        verbose_name = "آزمون"
        verbose_name_plural = "آزمون‌ها"

    def __str__(self):
        return self.title


class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="questions", verbose_name="آزمون")
    text = models.TextField(verbose_name="متن سوال")
    question_type = models.CharField(max_length=20, choices=consts.QUESTION_TYPES, verbose_name="نوع سوال")
    score = models.FloatField(verbose_name="نمره")

    class Meta:
        verbose_name = "سوال"
        verbose_name_plural = "سوالات"

    def __str__(self):
        return f"سوال {self.id} - {self.exam.title}"


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options", verbose_name="سوال")
    text = models.CharField(max_length=255, verbose_name="متن گزینه")
    is_correct = models.BooleanField(default=False, verbose_name="گزینه صحیح")

    class Meta:
        verbose_name = "گزینه"
        verbose_name_plural = "گزینه‌ها"

    def __str__(self):
        return f"{self.text}"


class UserAnswer(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="دانش‌آموز")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="سوال")
    answer_text = models.TextField(verbose_name="پاسخ داده‌شده")
    score = models.FloatField(null=True, blank=True, verbose_name="نمره اختصاص داده‌شده")

    class Meta:
        verbose_name = "پاسخ دانش‌آموز"
        verbose_name_plural = "پاسخ‌های دانش‌آموزان"


class UserOptions(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="دانش‌آموز")
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, verbose_name="آزمون")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="سوال")
    answer_option = models.ForeignKey(Option, on_delete=models.CASCADE, verbose_name="پاسخ داده شده")

    class Meta:
        verbose_name = "پاسخ تستی دانش‌آموز"
        verbose_name_plural = "پاسخ‌های تستی دانش‌آموزان"


class Feedback(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="دانش‌آموز")
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, verbose_name="آزمون")
    text = models.TextField(verbose_name="متن بازخورد")

    class Meta:
        verbose_name = "بازخورد"
        verbose_name_plural = "بازخوردها"

    def __str__(self):
        return f"بازخورد از {self.user} برای {self.exam}"
