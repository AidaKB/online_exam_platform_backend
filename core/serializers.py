# from rest_framework import serializers
# from core import models
# from contestant import models as contestant_models
# from . import exceptions
# from dj_rest_auth.serializers import LoginSerializer
# from django.contrib.auth import authenticate
#
# from .models import CustomUser
#
#
# class CustomUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.CustomUser
#         fields = ('id', 'username', 'email')
#
#
# class InstituteSignUpSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, max_length=255)
#     password2 = serializers.CharField(write_only=True, max_length=255)
#     team_name = serializers.CharField(write_only=True, max_length=255)
#
#     class Meta:
#         model = models.CustomUser
#         fields = ('id', 'username', 'password', 'password2', 'team_name')
#
#     def validate(self, attrs):
#         if attrs['password'] != attrs['password2']:
#             raise exceptions.PasswordISNotSameAsPassword2()
#         return attrs
#
#     def create(self, validated_data):
#         validated_data['is_team'] = True
#         if contestant_models.Team.objects.filter(name=validated_data['team_name']).exists():
#             raise exceptions.TeamNameAlreadyExist()
#         team_name = validated_data.pop('team_name')
#         validated_data.pop('password2')
#         team_account = CustomUser.objects.create_user(
#             username=validated_data.pop('username', None),
#             password=validated_data.pop('password', None),
#             **validated_data
#         )
#         contestant_models.Team.objects.create(
#             account=team_account,
#             name=team_name
#         )
#         return team_account
#
#
# class StaffSignUpSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, max_length=255)
#     password2 = serializers.CharField(write_only=True, max_length=255)
#
#     class Meta:
#         model = models.CustomUser
#         fields = ('id', 'username', 'password', 'password2', 'first_name', 'last_name', 'email')
#
#     def validate(self, attrs):
#         if attrs['password'] != attrs['password2']:
#             raise exceptions.PasswordISNotSameAsPassword2()
#         return attrs
#
#     def create(self, validated_data):
#         validated_data.pop('password2')
#         team = CustomUser.objects.create_superuser(
#             username=validated_data.pop('username', None),
#             password=validated_data.pop('password', None),
#             **validated_data
#         )
#         return team
#
#
# class CustomLoginSerializer(LoginSerializer):
#     username = serializers.CharField()
#     password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)
#
#     def validate(self, attrs):
#         username = attrs.get('username')
#         password = attrs.get('password')
#
#         if not username or not password:
#             raise exceptions.PasswordAndUsernameIsRequired()
#
#         user = authenticate(username=username, password=password)
#         if not user:
#             raise exceptions.PasswordOrUsernameIsIncorrect()
#
#         attrs['user'] = user
#         return attrs
