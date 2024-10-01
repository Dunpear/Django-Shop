from django.db import models
from django_jalali.db import models as jmodels
import jdatetime
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from colorfield.fields import ColorField

class SiteSettings(models.Model):
    site_title = models.CharField(max_length=500, verbose_name='عنوان سایت')
    site_description = RichTextField(config_name='special', blank=True, null=True, verbose_name='توضیحات سایت')
    favicon = models.ImageField(upload_to='favicons/', blank=True, null=True, verbose_name='آیکون سایت')
    co_address = models.CharField(max_length=1500, blank=True, null=True, verbose_name='آدرس پستی')
    about_me = RichTextUploadingField(config_name='special', blank=True, null=True, verbose_name='متن درباره ما')
    event_text = RichTextField(config_name='special', blank=True, null=True, verbose_name='متن ایونت')
    tel_number = models.CharField(max_length=50, blank=True, null=True, verbose_name='شماره تلفن')
    fax_number = models.CharField(max_length=15, blank=True, null=True, verbose_name='فکس')
    logo = models.ImageField(upload_to='logos/', verbose_name='لوگو سایت')
    logo_alt = models.CharField(max_length=100, blank=True, null=True, verbose_name='متن جایگزین لوگو')
    logo_title = models.CharField(max_length=200, blank=True, null=True, verbose_name='عنوان لوگو')
    width = models.IntegerField(null=True, blank=True, verbose_name='عرض لوگو')
    height = models.IntegerField(null=True, blank=True, verbose_name='ارتفاع لوگو')
    footer_color = models.CharField(max_length=80, blank=True, null=True, verbose_name='رنگ پانویس')
    header_color = models.CharField(max_length=80, blank=True, null=True, verbose_name='رنگ سربرگ')
    body_color = models.CharField(max_length=80, blank=True, null=True, verbose_name='رنگ زمینه')
    register_date = jmodels.jDateField(default=jdatetime.date.today(), verbose_name='تاریخ ساخت')
    background_advantage = models.ImageField(upload_to='advantages/', verbose_name='پس زمینه مزیت رقابتی', blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name='وضعیت')

    class Meta:
        verbose_name = 'تنظیم اولیه'
        verbose_name_plural = 'تنظیمات اولیه'

    def __str__(self):
        return f'Title : {self.site_title} - Telephone : {self.tel_number}'


class SocialMedia(models.Model):
    social_media_name = models.CharField(max_length=500, blank=True, null=True, verbose_name='نام شبکه اجتماعی')
    social_media_description = RichTextUploadingField(config_name='special', blank=True, null=True,
                                                      verbose_name='توضیحات شبکه اجتماعی')
    social_media_url = models.CharField(max_length=1000, blank=True, null=True, verbose_name='آدرس اینترنتی')
    social_media_image = models.ImageField(upload_to='social_media/', blank=True, null=True, verbose_name='لوگو')
    social_media_image_alt = models.CharField(max_length=100, blank=True, null=True, verbose_name='متن جایگزین لوگو')
    social_media_image_title = models.CharField(max_length=200, blank=True, null=True, verbose_name='عنوان لوگو')
    width = models.IntegerField(null=True, blank=True, verbose_name='عرض لوگو')
    height = models.IntegerField(null=True, blank=True, verbose_name='ارتفاع لوگو')
    css_class = models.CharField(max_length=250, blank=True, null=True, verbose_name='کلاس اضافی')
    css_style = models.CharField(max_length=1000, blank=True, null=True, verbose_name='استایل اضافی')
    register_date = jmodels.jDateField(default=jdatetime.date.today(), verbose_name='تاریخ ساخت')
    is_active = models.BooleanField(default=True, verbose_name='وضعیت')

    class Meta:
        verbose_name = 'شبکه اجتماعی'
        verbose_name_plural = 'شبکه های اجتماعی'

    def __str__(self):
        return f'Social Media Title: {self.social_media_name}'


class RepetitiveQuestions(models.Model):
    repetitive_question = models.CharField(max_length=3000, blank=True, null=True, verbose_name='متن سوال')
    repetitive_answer = RichTextUploadingField(config_name='special', blank=True, null=True, verbose_name='جواب سوال')
    register_date = jmodels.jDateField(default=jdatetime.date.today(), verbose_name='تاریخ ساخت')
    is_active = models.BooleanField(default=True, verbose_name='وضعیت')

    class Meta:
        verbose_name = 'سوال تکراری'
        verbose_name_plural = 'سوالات تکراری'

    def __str__(self):
        return self.repetitive_question


class SiteRules(models.Model):
    site_rule_name = models.CharField(max_length=10000, blank=True, null=True, verbose_name='نام قرارداد')
    site_rule_description = RichTextUploadingField(config_name='special', blank=True, null=True,
                                                   verbose_name='متن قرارداد')
    register_date = jmodels.jDateField(default=jdatetime.date.today(), verbose_name='تاریخ ساخت')
    is_active = models.BooleanField(default=True, verbose_name='وضعیت')

    class Meta:
        verbose_name = 'قانون سایت'
        verbose_name_plural = 'قوانین سایت'

    def __str__(self):
        return self.site_rule_name



class Advantages(models.Model):
    advantage_name = models.CharField(max_length=200, verbose_name='نام مزیت رقابتی')
    image = models.ImageField(upload_to='advantages/icons', verbose_name='آیکون مزیت رقابتی', blank=True, null=True)
    color = ColorField(default='#FF0000', verbose_name='رنگ پس زمینه')
    advantage_description = RichTextUploadingField(config_name='special', blank=True, verbose_name='توضیحات')
    register_date = jmodels.jDateField(default=jdatetime.date.today(), verbose_name='تاریخ ثبت')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیر فعال')

    def __str__(self):
        return self.advantage_name

    class Meta:
        verbose_name = 'مزیت رقابتی'
        verbose_name_plural = 'مزیت های رقابتی'
