# Generated by Django 5.0.3 on 2024-04-08 15:03

import datetime
import django_jalali.db.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_alter_brand_register_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_mixin',
            field=models.BooleanField(default=False, verbose_name='فروش این محصول به عنوان ترکیب'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='register_date',
            field=django_jalali.db.models.jDateField(default=datetime.date(2024, 4, 8), verbose_name='تاریخ ساخت'),
        ),
        migrations.AlterField(
            model_name='product',
            name='register_date',
            field=django_jalali.db.models.jDateField(default=datetime.date(2024, 4, 8), verbose_name='تاریخ درج'),
        ),
        migrations.AlterField(
            model_name='product',
            name='updated_date',
            field=django_jalali.db.models.jDateField(default=datetime.date(2024, 4, 8), verbose_name='تاریخ آخرین بروزرسانی'),
        ),
        migrations.AlterField(
            model_name='productgroup',
            name='register_date',
            field=django_jalali.db.models.jDateField(default=datetime.date(2024, 4, 8), verbose_name='تاریخ ساخت'),
        ),
    ]