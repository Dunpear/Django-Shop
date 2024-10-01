# Generated by Django 5.0.3 on 2024-03-17 07:47

import datetime
import django_jalali.db.models
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0011_alter_invoice_register_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='register_date',
            field=django_jalali.db.models.jDateField(default=datetime.date(2024, 3, 17), verbose_name='تاریخ فاکتور'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='tracking_code',
            field=models.UUIDField(default=uuid.UUID('17a334fd-61ae-4138-98d3-135af75af71d'), editable=False, unique=True, verbose_name='کد پیگیری'),
        ),
    ]