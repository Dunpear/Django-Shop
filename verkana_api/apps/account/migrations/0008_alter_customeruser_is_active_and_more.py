# Generated by Django 5.0.3 on 2024-03-25 19:38

import datetime
import django_jalali.db.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_customeruser_image_alter_customeruser_register_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customeruser',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='وضعیت کاربر'),
        ),
        migrations.AlterField(
            model_name='customeruser',
            name='register_date',
            field=django_jalali.db.models.jDateField(default=datetime.date(2024, 3, 25), verbose_name='تاریخ ثبت نام'),
        ),
    ]
