# Generated by Django 5.0.4 on 2024-04-28 14:10

import datetime
import django_jalali.db.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_alter_blog_register_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='register_date',
            field=django_jalali.db.models.jDateField(default=datetime.date(2024, 4, 28), verbose_name='تاریخ ساخت'),
        ),
        migrations.AlterField(
            model_name='blogcategory',
            name='register_date',
            field=django_jalali.db.models.jDateField(default=datetime.date(2024, 4, 28), verbose_name='تاریخ ساخت'),
        ),
        migrations.AlterField(
            model_name='blogtag',
            name='register_date',
            field=django_jalali.db.models.jDateField(default=datetime.date(2024, 4, 28), verbose_name='تاریخ ساخت'),
        ),
    ]