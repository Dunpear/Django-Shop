# Generated by Django 5.0.3 on 2024-03-12 11:01

import datetime
import django_jalali.db.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('slider', '0002_alter_slider_register_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slider',
            name='register_date',
            field=django_jalali.db.models.jDateField(default=datetime.date(2024, 3, 12), verbose_name='تاریخ ساخت'),
        ),
        migrations.AlterField(
            model_name='slideritem',
            name='register_date',
            field=django_jalali.db.models.jDateField(default=datetime.date(2024, 3, 12), verbose_name='تاریخ ساخت'),
        ),
    ]