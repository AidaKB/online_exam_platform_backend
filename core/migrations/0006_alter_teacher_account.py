# Generated by Django 4.2.23 on 2025-06-27 11:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_teacher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='account',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='teachers', to=settings.AUTH_USER_MODEL, verbose_name='حساب کاربری'),
        ),
    ]
