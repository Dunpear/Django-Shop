# Generated by Django 5.0.2 on 2024-03-10 14:45

import datetime
import django.db.models.deletion
import django_jalali.db.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('invoice', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SellerSelling',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amount', models.IntegerField(verbose_name='مبلغ پرداخت شده')),
                ('is_calculation', models.BooleanField(default=False, verbose_name='محاسبه شد / محاسبه نشد')),
                ('register_date', django_jalali.db.models.jDateField(default=datetime.date(2024, 3, 10), verbose_name='تاریخ فاکتور')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='invoice_selling_seller', to='invoice.invoice', verbose_name='فاکتور')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_selling_seller', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'فروش فروشنده',
                'verbose_name_plural': 'فروش فروشندگان',
            },
        ),
        migrations.CreateModel(
            name='SellerTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_sell_amount', models.DecimalField(decimal_places=0, help_text='این مبلغ کل وجه بدون کم کردن پورسانت میباشد!', max_digits=15, verbose_name='جمع فروش')),
                ('commission_percentage', models.SmallIntegerField(verbose_name='درصد پورسانت')),
                ('commission_amount', models.DecimalField(decimal_places=0, max_digits=15, verbose_name='مبلغ پورسانت')),
                ('last_amount_receivable', models.DecimalField(decimal_places=0, max_digits=15, verbose_name='مبلغ آخرین دریافت')),
                ('remaining_amount', models.DecimalField(blank=True, decimal_places=0, max_digits=15, null=True, verbose_name='مبلغ مانده')),
                ('last_received_date', django_jalali.db.models.jDateField(blank=True, null=True, verbose_name='')),
                ('is_money_requested', models.BooleanField(default=False, verbose_name='درخواست دریافت وجه')),
                ('mony_request', models.DecimalField(decimal_places=0, max_digits=15, verbose_name='مبلغ درخواستی')),
                ('mony_request_date', django_jalali.db.models.jDateField(blank=True, null=True, verbose_name='تاریخ درخواست وجه')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_seller', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'تراکنش فروشنده',
                'verbose_name_plural': 'تراکنش های فروشندگان',
            },
        ),
    ]