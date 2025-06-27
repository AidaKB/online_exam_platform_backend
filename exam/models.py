from django.db import models
from core.models import Student,Teacher,Institute
from . import consts


class Classroom(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="نام کلاس"
    )
    institute = models.ForeignKey(
        Institute,
        on_delete=models.CASCADE,
        related_name="classrooms",
        verbose_name="آموزشگاه"
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="classrooms",
        verbose_name="استاد"
    )
    grade = models.CharField(
        max_length=30,
        choices=consts.GRADE_CHOICES,
        verbose_name="پایه تحصیلی"
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name="توضیحات"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )

    class Meta:
        verbose_name = "کلاس"
        verbose_name_plural = "کلاس‌ها"

    def __str__(self):
        return f"{self.name} - {self.grade} ({self.institute.name})"


class StudentClassroom(models.Model):
    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.PROTECT,
        related_name="student_classroom",
        verbose_name="کلاس"
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.PROTECT,
        related_name="student_classroom",
        verbose_name="دانشجو"
    )


class Major(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام رشته تحصیلی")

    def __str__(self):
        return self.name
