from django.db import models
from django_jalali.db import models as jmodels
import jdatetime
from ckeditor.fields import RichTextField


class Slider(models.Model):
    title = models.CharField(max_length=250, blank=True, null=True, verbose_name='عنوان اسلایدر')
    register_date = jmodels.jDateField(default=jdatetime.date.today(), verbose_name='تاریخ ساخت')
    delay = models.IntegerField(blank=True, null=True, verbose_name='مدت زمان تعویض')
    auto_play = models.BooleanField(default=True, verbose_name='شروع خودکار')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')

    class Meta:
        verbose_name = 'اسلایدر'
        verbose_name_plural = 'اسلایدرها'

    def __str__(self):
        return self.title


class SliderItem(models.Model):
    title = models.CharField(max_length=250, blank=True, null=True, verbose_name='عنوان اسلایدر')
    description = RichTextField(config_name='special', blank=True, null=True, verbose_name='توضیحات اسلایدر')
    link = models.URLField(max_length=600, blank=True, null=True, verbose_name='لینک')
    link_title = models.CharField(max_length=250, blank=True, null=True, verbose_name='عنوان لینک')
    picture = models.ImageField(upload_to='sliders/', verbose_name='عکس اسلایدر')
    picture_alt = models.CharField(max_length=250, blank=True, null=True, verbose_name='متن جایگزین')
    picture_title = models.CharField(max_length=250, blank=True, null=True, verbose_name='عنوان تصویر')
    width = models.IntegerField(null=True, blank=True, verbose_name='عرض تصویر')
    height = models.IntegerField(null=True, blank=True, verbose_name='ارتفاع تصوبر')
    css_class = models.CharField(max_length=300, blank=True, null=True, verbose_name='کلاس نماشی')
    css_style = models.CharField(max_length=500, blank=True, null=True, verbose_name='استایل نمایشی')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')
    register_date = jmodels.jDateField(default=jdatetime.date.today(), verbose_name='تاریخ ساخت')
    slider = models.ForeignKey(Slider, on_delete=models.CASCADE, related_name='slider_items')

    class Meta:
        verbose_name = 'آیتم اسلایدر'
        verbose_name_plural = 'آیتم اسلایدر ها'

    def __str__(self):
        return self.title
