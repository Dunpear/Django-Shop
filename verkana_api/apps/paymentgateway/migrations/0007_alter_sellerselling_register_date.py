# Generated by Django 5.0.3 on 2024-03-17 07:47

import datetime
import django_jalali.db.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paymentgateway', '0006_alter_sellerselling_register_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellerselling',
            name='register_date',
            field=django_jalali.db.models.jDateField(default=datetime.date(2024, 3, 17), verbose_name='تاریخ فاکتور'),
        ),
    ]