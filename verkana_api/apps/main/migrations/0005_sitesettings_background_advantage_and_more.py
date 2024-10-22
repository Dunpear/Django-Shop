# Generated by Django 5.0.3 on 2024-03-14 17:27

import datetime
import django_jalali.db.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_repetitivequestions_register_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='background_advantage',
            field=models.ImageField(blank=True, null=True, upload_to='advantages/', verbose_name='پس زمینه مزیت رقابتی'),
        ),
        migrations.AlterField(
            model_name='repetitivequestions',
            name='register_date',
            field=django_jalali.db.models.jDateField(default=datetime.date(2024, 3, 14), verbose_name='تاریخ ساخت'),
        ),
        migrations.AlterField(
            model_name='siterules',
            name='register_date',
            field=django_jalali.db.models.jDateField(default=datetime.date(2024, 3, 14), verbose_name='تاریخ ساخت'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='register_date',
            field=django_jalali.db.models.jDateField(default=datetime.date(2024, 3, 14), verbose_name='تاریخ ساخت'),
        ),
        migrations.AlterField(
            model_name='socialmedia',
            name='register_date',
            field=django_jalali.db.models.jDateField(default=datetime.date(2024, 3, 14), verbose_name='تاریخ ساخت'),
        ),
    ]
