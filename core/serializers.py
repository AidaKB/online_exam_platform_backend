from rest_framework import serializers
from . import models
from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth import authenticate

from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = ('id', 'username', 'email')


class AdminSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, max_length=255)
    password2 = serializers.CharField(write_only=True, max_length=255)

    class Meta:
        model = models.CustomUser
        fields = ('id', 'username', 'password', 'password2', 'first_name', 'last_name', 'email')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                'password': 'رمز عبور و تکرار آن یکسان نیستند.'
            })
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        admin = CustomUser.objects.create_superuser(
            username=validated_data.pop('username', None),
            password=validated_data.pop('password', None),
            **validated_data
        )
        return admin


class InstituteSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, max_length=255)
    password2 = serializers.CharField(write_only=True, max_length=255)

    institute_name = serializers.CharField(write_only=True, max_length=255)
    registration_code = serializers.CharField(write_only=True, max_length=50)
    address = serializers.CharField(write_only=True, style={'base_template': 'textarea.html'}, max_length=1000,
                                    allow_blank=True)
    phone = serializers.CharField(write_only=True, max_length=20)
    website = serializers.URLField(write_only=True, allow_null=True, allow_blank=True)

    class Meta:
        model = models.CustomUser
        fields = ('id',
                  'username',
                  'password',
                  'password2',
                  'email',
                  'institute_name',
                  'registration_code',
                  'address',
                  'phone',
                  'website',
                  )

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                'password': 'رمز عبور و تکرار آن یکسان نیستند.'
            })
        return attrs

    def create(self, validated_data):
        validated_data['user_type'] = 'institute'
        if models.Institute.objects.filter(name=validated_data['institute_name']).exists():
            raise serializers.ValidationError({
                'institute_name': 'آموزشگاهی با این نام قبلاً ثبت شده است.'
            })
        institute_name = validated_data.pop('institute_name')
        registration_code = validated_data.pop('registration_code')
        address = validated_data.pop('address')
        phone = validated_data.pop('phone')
        website = validated_data.pop('website')
        validated_data.pop('password2')
        institute_account = CustomUser.objects.create_user(
            username=validated_data.pop('username', None),
            password=validated_data.pop('password', None),
            **validated_data
        )
        models.Institute.objects.create(
            account=institute_account,
            name=institute_name,
            registration_code=registration_code,
            address=address,
            phone=phone,
            website=website
        )
        return institute_account


class InstituteSerializer(serializers.ModelSerializer):
    account = CustomUserSerializer(read_only=True)

    class Meta:
        model = models.Institute
        fields = (
            'id',
            'account',
            'name',
            'registration_code',
            'address',
            'phone',
            'website',
            'created_at',
        )


class TeacherSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, max_length=255)
    password2 = serializers.CharField(write_only=True, max_length=255)

    institute_id = serializers.IntegerField(write_only=True, required=True)
    national_code = serializers.CharField(write_only=True, max_length=10, required=True)
    phone_number = serializers.CharField(write_only=True, max_length=20, required=True)
    expertise = serializers.CharField(write_only=True, max_length=100, required=True)

    class Meta:
        model = models.CustomUser
        fields = (
            'id', 'username', 'password', 'password2', 'institute_id', 'first_name', 'last_name', 'national_code',
            'phone_number', 'expertise'
        )

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                'password': 'رمز عبور و تکرار آن یکسان نیستند.'
            })
        return attrs

    def create(self, validated_data):
        validated_data['user_type'] = 'teacher'

        institute_id = validated_data.pop('institute_id')
        national_code = validated_data.pop('national_code')
        phone_number = validated_data.pop('phone_number')
        expertise = validated_data.pop('expertise')

        validated_data.pop('password2')
        teacher_account = CustomUser.objects.create_user(
            username=validated_data.pop('username', None),
            password=validated_data.pop('password', None),
            **validated_data
        )
        models.Teacher.objects.create(
            account=teacher_account,
            institute_id=institute_id,
            national_code=national_code,
            phone_number=phone_number,
            expertise=expertise,
        )
        return teacher_account


class TeacherSerializer(serializers.ModelSerializer):
    account = CustomUserSerializer(read_only=True)
    institute = InstituteSerializer(read_only=True)

    class Meta:
        model = models.Teacher
        fields = (
            'id',
            'account',
            'institute',
            'national_code',
            'phone_number',
            'expertise',
            'created_at',
        )


class StudentSerializer(serializers.ModelSerializer):
    account = CustomUserSerializer(read_only=True)
    institute = InstituteSerializer(read_only=True)

    class Meta:
        model = models.Student
        fields = (
            'id',
            'account',
            'institute',
            'national_code',
            'phone_number',
            'major',
            'date_of_birth',
            'gender',
            'created_at',
        )


class StudentSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, max_length=255)
    password2 = serializers.CharField(write_only=True, max_length=255)

    institute_id = serializers.IntegerField(write_only=True, required=True)
    national_code = serializers.CharField(write_only=True, max_length=10, required=True)
    phone_number = serializers.CharField(write_only=True, max_length=20, required=True)
    major_id = serializers.IntegerField(write_only=True, required=True)
    date_of_birth = serializers.DateField(write_only=True, allow_null=True)
    gender = serializers.CharField(write_only=True, max_length=10, required=True, allow_blank=True, allow_null=True)

    class Meta:
        model = models.CustomUser
        fields = (
            'id', 'username', 'password', 'password2', 'institute_id', 'first_name', 'last_name', 'national_code',
            'phone_number', 'major_id', 'date_of_birth', 'gender'
        )

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                'password': 'رمز عبور و تکرار آن یکسان نیستند.'
            })
        return attrs

    def create(self, validated_data):
        validated_data['user_type'] = 'student'

        institute_id = validated_data.pop('institute_id')
        national_code = validated_data.pop('national_code')
        phone_number = validated_data.pop('phone_number')
        major_id = validated_data.pop('major_id')
        date_of_birth = validated_data.pop('date_of_birth')
        gender = validated_data.pop('gender')

        validated_data.pop('password2')
        student_account = CustomUser.objects.create_user(
            username=validated_data.pop('username', None),
            password=validated_data.pop('password', None),
            **validated_data
        )
        models.Student.objects.create(
            account=student_account,
            institute_id=institute_id,
            national_code=national_code,
            phone_number=phone_number,
            major_id=major_id,
            date_of_birth=date_of_birth,
            gender=gender,
        )
        return student_account


class CustomLoginSerializer(LoginSerializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if not username or not password:
            raise serializers.ValidationError(
                {"detail": "وارد کردن نام کاربری و رمز عبور الزامی است."},
                code='authorization'
            )

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError(
                {"detail": "نام کاربری یا رمز عبور نادرست است."},
                code='authorization'
            )

        attrs['user'] = user
        return attrs
