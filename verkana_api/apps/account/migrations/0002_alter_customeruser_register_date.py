# Generated by Django 5.0.2 on 2024-03-11 07:35

import datetime
import django_jalali.db.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customeruser',
            name='register_date',
            field=django_jalali.db.models.jDateField(default=datetime.date(2024, 3, 11), verbose_name='تاریخ ثبت نام'),
        ),
    ]
