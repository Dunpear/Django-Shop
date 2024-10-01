from django.db import models
from django_jalali.db import models as jmodels
import jdatetime
from apps.account.models import CustomerUser
from django.utils.html import mark_safe
from apps.invoice.models import Invoice
from apps.product.models import Product


class SellerSelling(models.Model):
    total_amount = models.IntegerField(verbose_name='مبلغ پرداخت شده')
    is_calculation = models.BooleanField(default=False, verbose_name='محاسبه شد / محاسبه نشد')
    register_date = jmodels.jDateField(default=jdatetime.date.today(), verbose_name='تاریخ فاکتور')
    user = models.ForeignKey(CustomerUser, on_delete=models.PROTECT, verbose_name='کاربر',
                             related_name='user_selling_seller')
    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT, verbose_name='فاکتور',
                                related_name='invoice_selling_seller')

    class Meta:
        verbose_name = 'فروش فروشنده'
        verbose_name_plural = 'فروش فروشندگان'

    def __str__(self):
        return f'Seller : {self.user.name} - Amount :{str(self.total_amount)}'


class SellerTransaction(models.Model):
    total_sell_amount = models.DecimalField(max_digits=15, decimal_places=0, verbose_name='جمع فروش',
                                            help_text='این مبلغ کل وجه بدون کم کردن پورسانت میباشد!')
    commission_percentage = models.SmallIntegerField(verbose_name='درصد پورسانت')
    commission_amount = models.DecimalField(max_digits=15, decimal_places=0, verbose_name='مبلغ پورسانت')
    last_amount_receivable = models.DecimalField(max_digits=15, decimal_places=0, verbose_name='مبلغ آخرین دریافت', blank=True, null=True)
    remaining_amount = models.DecimalField(max_digits=15, decimal_places=0, verbose_name='مبلغ مانده', null=True,
                                           blank=True)
    last_received_date = jmodels.jDateField(verbose_name='', null=True, blank=True)
    is_money_requested = models.BooleanField(default=False, verbose_name='درخواست دریافت وجه')
    mony_request = models.DecimalField(max_digits=15, decimal_places=0, verbose_name='مبلغ درخواستی', null=True, blank=True)
    mony_request_date = jmodels.jDateField(verbose_name='تاریخ درخواست وجه', null=True, blank=True)

    user = models.ForeignKey(CustomerUser, on_delete=models.PROTECT, verbose_name='کاربر',
                             related_name='user_seller')

    def __str__(self):
        return f'Seller : {self.user.name} - Amount : {self.total_sell_amount}'

    class Meta:
        verbose_name = 'تراکنش فروشنده'
        verbose_name_plural = 'تراکنش های فروشندگان'
