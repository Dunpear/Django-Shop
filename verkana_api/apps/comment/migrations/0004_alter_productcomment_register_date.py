# Generated by Django 5.0.3 on 2024-03-13 07:01

import datetime
import django_jalali.db.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0003_alter_productcomment_register_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcomment',
            name='register_date',
            field=django_jalali.db.models.jDateField(default=datetime.date(2024, 3, 13), verbose_name='تاریخ درج'),
        ),
    ]
