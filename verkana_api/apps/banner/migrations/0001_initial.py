# Generated by Django 5.0.2 on 2024-03-10 14:45

import ckeditor.fields
import datetime
import django_jalali.db.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='عنوان بنر')),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='توضیحات')),
                ('picture', models.ImageField(upload_to='banners/', verbose_name='تصویر')),
                ('picture_alt', models.CharField(blank=True, max_length=250, null=True, verbose_name='متن جایگزین تصویر')),
                ('picture_title', models.CharField(blank=True, max_length=250, null=True, verbose_name='عنوان تصویر')),
                ('width', models.IntegerField(blank=True, null=True, verbose_name='عرض تصویر')),
                ('height', models.IntegerField(blank=True, null=True, verbose_name='ارتفاع تصوبر')),
                ('link', models.URLField(blank=True, max_length=600, null=True, verbose_name='لینک')),
                ('link_title', models.CharField(blank=True, max_length=250, null=True, verbose_name='عنوان لینک')),
                ('css_class', models.CharField(blank=True, max_length=250, null=True, verbose_name='کلاس اضافی')),
                ('css_style', models.CharField(blank=True, max_length=700, null=True, verbose_name='استایل اضافی')),
                ('is_active', models.BooleanField(default=True, verbose_name='وضعیت')),
                ('register_date', django_jalali.db.models.jDateField(default=datetime.date(2024, 3, 10), verbose_name='تاریخ ساخت')),
            ],
            options={
                'verbose_name': 'بنر',
                'verbose_name_plural': 'بنرها',
            },
        ),
    ]
