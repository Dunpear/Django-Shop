from django.db import models
from django_jalali.db import models as jmodels
import jdatetime
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField


class Banner(models.Model):
    title = models.CharField(max_length=250, verbose_name='عنوان بنر')
    description = RichTextField(config_name='special', blank=True, null=True, verbose_name='توضیحات')
    picture = models.ImageField(upload_to='banners/', verbose_name='تصویر')
    picture_alt = models.CharField(max_length=250, blank=True, null=True, verbose_name='متن جایگزین تصویر')
    picture_title = models.CharField(max_length=250, blank=True, null=True, verbose_name='عنوان تصویر')
    width = models.IntegerField(null=True, blank=True, verbose_name='عرض تصویر')
    height = models.IntegerField(null=True, blank=True, verbose_name='ارتفاع تصوبر')
    link = models.URLField(max_length=600, blank=True, null=True, verbose_name='لینک')
    link_title = models.CharField(max_length=250, blank=True, null=True, verbose_name='عنوان لینک')
    css_class = models.CharField(max_length=250, blank=True, null=True, verbose_name='کلاس اضافی')
    css_style = models.CharField(max_length=700, blank=True, null=True, verbose_name='استایل اضافی')
    is_active = models.BooleanField(default=True, verbose_name='وضعیت')
    register_date = jmodels.jDateField(default=jdatetime.date.today(), verbose_name='تاریخ ساخت')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'بنر'
        verbose_name_plural = 'بنرها'
