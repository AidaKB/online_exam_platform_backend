# Generated by Django 4.2.23 on 2025-06-26 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='ایمیل'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='نام'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='نام خانوادگی'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('institute', 'موسسه'), ('teacher', 'استاد'), ('student', 'دانشجو'), ('admin', 'مدیر سامانه')], default='admin', max_length=20, verbose_name='نوع کاربر'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(max_length=255, unique=True, verbose_name='نام کاربری'),
        ),
    ]
