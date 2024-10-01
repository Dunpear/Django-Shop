# Generated by Django 5.0.3 on 2024-03-15 18:49

import datetime
import django_jalali.db.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('banner', '0005_alter_banner_register_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='register_date',
            field=django_jalali.db.models.jDateField(default=datetime.date(2024, 3, 15), verbose_name='تاریخ ساخت'),
        ),
    ]
