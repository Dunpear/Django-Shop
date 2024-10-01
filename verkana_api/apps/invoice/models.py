from django.db import models
from apps.product.models import Product
from apps.account.models import CustomerUser
from django_jalali.db import models as jmodels
import jdatetime
from django.utils.html import mark_safe
from apps import utilities
from uuid import uuid4
from django.utils.crypto import get_random_string


class Invoice(models.Model):
    tax_amount = models.IntegerField(blank=True, null=True, verbose_name='مقدار مالیات')
    payable_amount = models.DecimalField(max_digits=15, decimal_places=0, verbose_name='مبلغ قابل پرداخت')
    receiver_address = models.TextField(verbose_name='آدرس گیرنده')
    received_phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='شماره تماس گیرنده')
    received_full_name = models.CharField(max_length=150, blank=True, null=True, verbose_name='نام گیرنده')
    postal_code = models.CharField(max_length=20, blank=True, null=True, verbose_name='کدپستی')
    invoice_description = models.TextField(blank=True, null=True, verbose_name='توضیحات فاکتور')
    is_pay = models.BooleanField(default=False, verbose_name='پرداخت / عدم پرداخت')
    ref_id = models.CharField(max_length=500, blank=True, null=True, verbose_name='Ref Id')
    authority = models.CharField(max_length=500, blank=True, null=True, verbose_name='authority')
    tracking_code = models.CharField(max_length=8, unique=True, default=get_random_string(allowed_chars='1234567890', length=7), verbose_name='کد پیگیری')
    register_date = jmodels.jDateField(default=jdatetime.date.today(), verbose_name='تاریخ فاکتور')
    delivery_date = jmodels.jDateField(blank=True, null=True, verbose_name='تاریخ تحویل')
    is_returned = models.BooleanField(default=False, verbose_name='برگشتی')
    returned_date = jmodels.jDateField(blank=True, null=True, verbose_name='تاریخ مرجوع')
    INVOICE_STATUS = (
        ('0', 'سبد خرید'), ('1', 'در حال پیگیری'), ('2', 'تایید شده'), ('3', 'تحویل به پست'), ('4', 'تحویل به مشتری'))
    invoice_status = models.CharField(max_length=200, choices=INVOICE_STATUS, default='0', verbose_name='وضعیت سفارش')

    user = models.ForeignKey(CustomerUser, on_delete=models.PROTECT, related_name='invoice_user', verbose_name='کاربر')

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'

    def __str__(self):
        return f'{self.id} - {str(self.register_date)}'

    def get_item(self):
        return mark_safe(
            f'<a style="border-radius: 5px;background-color: #417690;padding: 5px 11px;font-weight: 450; color:#fff;" href="{utilities.base_url}admin/invoice/invoiceitem/?invoice_id={self.id}">جزئیات</a>')

    get_item.short_description = ''
    get_item.allow_tags = True


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT, related_name='invoice_items', verbose_name='سفارش')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='product_item', verbose_name='محصول')
    count = models.PositiveIntegerField(verbose_name='تعداد')
    price = models.IntegerField(default=0, verbose_name='قیمت محصول')

    class Meta:
        verbose_name = 'محصول سفارش'
        verbose_name_plural = 'محصولات سفارش'

    def __str__(self):
        return f'{self.product} - {self.count} - {self.invoice}'

    def get_cover(self):
        return mark_safe(
            '<img src="/media/%s" width="50" height="50" style="border-radius:5px;" />' % (
                self.product.cover_picture))

    get_cover.short_description = 'کاور محصول'
    get_cover.allow_tags = True

    def get_seller(self):
        if self.product.user == None:
            return mark_safe(
                f'<p>ورکانا</p>')
        else:
            return mark_safe(
                f'<p>{self.product.user.name}</p>')

    get_seller.short_description = 'فروشنده'
    get_seller.allow_tags = True

    def get_price(self):
        number ="{:,.0f}".format(self.product.product_after_discount)
        return mark_safe(
            f'<p>{number}  ریال  </p>')

    get_price.short_description = 'قیمت فروش'
    get_price.allow_tags = True


class InvoiceLog(models.Model):
    log_type = models.TextField(verbose_name='متن گزارش')
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='invoice_logs',
                                verbose_name='گزارش سفارش')
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE, related_name='user_logs', verbose_name='کاربر')

    class Meta:
        verbose_name = "گزارش سفارش"
        verbose_name_plural = "گزارشات سسفارش"

    def __str__(self):
        return self.log_type


class Mixed(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT, related_name='mixed_item', verbose_name='سفارش')
    total_price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='قیمت کل ترکیب')


    class Meta:
        verbose_name = 'ترکیب'
        verbose_name_plural = 'لیست ترکیب ها'

    def __str__(self):
        return f'{self.invoice.user}'


class MixedItem(models.Model):
    mix = models.ForeignKey(Mixed, on_delete=models.PROTECT, related_name='mix_items', verbose_name='سفارش', null=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='mix_product_item', verbose_name='محصول')
    count = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='تعداد')
    total_price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='قیمت ترکیب')

    class Meta:
        verbose_name = 'محصول ترکیب'
        verbose_name_plural = 'محصولات ترکیب'

    def __str__(self):
        return f'{self.product}'