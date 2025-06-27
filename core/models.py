from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin

from . import consts
from .managers import CustomUserManager


class CustomUser(AbstractUser, PermissionsMixin):
    user_type = models.CharField(max_length=20, choices=consts.USER_TYPE_CHOICES, default="admin",
                                 verbose_name="نوع کاربر")
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=254)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_team = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'username'
    objects = CustomUserManager()

    def __str__(self):
        return self.username


class Institute(models.Model):
    account = models.OneToOneField(
        CustomUser, on_delete=models.PROTECT, related_name="institute", verbose_name="حساب کاربری")
    name = models.CharField(max_length=255, verbose_name="نام آموزشگاه")
    registration_code = models.CharField(max_length=50, unique=True, verbose_name="کد ثبت آموزشگاه")
    address = models.TextField(verbose_name="آدرس")
    phone = models.CharField(max_length=20, verbose_name="شماره تماس")
    website = models.URLField(null=True, blank=True, verbose_name="وب‌سایت")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")

    class Meta:
        verbose_name = "آموزشگاه"
        verbose_name_plural = "آموزشگاه‌ها"

    def __str__(self):
        return self.name


class Teacher(models.Model):
    account = models.OneToOneField(
        CustomUser, on_delete=models.PROTECT, related_name="teacher", verbose_name="حساب کاربری")
    institute = models.ForeignKey(
        Institute,
        on_delete=models.CASCADE,
        related_name="teachers",
        verbose_name="آموزشگاه"
    )
    national_code = models.CharField(max_length=10, unique=True, verbose_name="کد ملی")
    phone_number = models.CharField(max_length=20, verbose_name="شماره تماس")
    expertise = models.CharField(max_length=100, verbose_name="تخصص")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ عضویت")

    class Meta:
        verbose_name = "استاد"
        verbose_name_plural = "اساتید"

    def __str__(self):
        return f"{self.account.get_full_name()} - {self.expertise}"


class Student(models.Model):
    account = models.OneToOneField(
        CustomUser, on_delete=models.PROTECT, related_name="student", verbose_name="حساب کاربری")
    institute = models.ForeignKey(
        Institute,
        on_delete=models.CASCADE,
        related_name="students",
        verbose_name="آموزشگاه"
    )
    national_code = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="کد ملی"
    )
    phone_number = models.CharField(
        max_length=20,
        verbose_name="شماره تماس"
    )
    major = models.ForeignKey(
        'exam.Major',
        on_delete=models.PROTECT,
        verbose_name="رشته تحصیلی"
    )
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        verbose_name="تاریخ تولد"
    )
    gender = models.CharField(
        max_length=10,
        choices=consts.GENDER_CHOICES,
        null=True,
        blank=True,
        verbose_name="جنسیت"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ عضویت"
    )

    class Meta:
        verbose_name = "دانش‌آموز"
        verbose_name_plural = "دانش‌آموزان"

    def __str__(self):
        return f"{self.account.get_full_name()} - {self.major}"
