from rest_framework import serializers
from . import models
from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth import authenticate

from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = ('id', 'username', 'email')


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


class StaffSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, max_length=255)
    password2 = serializers.CharField(write_only=True, max_length=255)

    class Meta:
        model = models.CustomUser
        fields = ('id', 'username', 'password', 'password2', 'first_name', 'last_name', 'email')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise exceptions.PasswordISNotSameAsPassword2()
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        team = CustomUser.objects.create_superuser(
            username=validated_data.pop('username', None),
            password=validated_data.pop('password', None),
            **validated_data
        )
        return team


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
