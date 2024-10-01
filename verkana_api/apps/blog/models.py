from django.db import models
from django_jalali.db import models as jmodels
import jdatetime
from ckeditor_uploader.fields import RichTextUploadingField


class BlogCategory(models.Model):
    title = models.CharField(max_length=250, unique=True, verbose_name='عنوان دسته بندی')
    slug = models.SlugField(unique=True, verbose_name='متن در آدرس slug')
    is_active = models.BooleanField(default=True, verbose_name='وضعیت')
    register_date = jmodels.jDateField(default=jdatetime.date.today(), verbose_name='تاریخ ساخت')
    picture = models.ImageField(upload_to='blog/category/', null=True, blank=True, verbose_name='تصویر دسته بندی')
    picture_alt = models.CharField(max_length=250, null=True, blank=True, verbose_name='متن جایگزین')
    picture_title = models.CharField(max_length=250, null=True, blank=True, verbose_name='عنوان تصویر')
    width = models.IntegerField(null=True, blank=True, verbose_name='عرض تصویر')
    height = models.IntegerField(null=True, blank=True, verbose_name='ارتفاع تصوبر')

    class Meta:
        verbose_name = 'دسته بندی مقاله'
        verbose_name_plural = 'دسته بندی مقاله ها'

    def __str__(self):
        return self.title


class Blog(models.Model):
    title = models.CharField(max_length=250, verbose_name='عنوان مقاله')
    description = RichTextUploadingField(config_name='special', verbose_name='توضیحات')
    picture = models.ImageField(upload_to='blog/article', null=True, blank=True, verbose_name='تصویر مقاله')
    picture_alt = models.CharField(max_length=250, null=True, blank=True, verbose_name='متن جایگزین')
    picture_title = models.CharField(max_length=250, null=True, blank=True, verbose_name='عنوان تصویر')
    width = models.IntegerField(null=True, blank=True, verbose_name='عرض تصویر')
    height = models.IntegerField(null=True, blank=True, verbose_name='ارتفاع تصوبر')
    meta_keyword = models.CharField(max_length=700, null=True, blank=True, verbose_name='Meta Keyword')
    meta_description = models.CharField(max_length=700, null=True, blank=True, verbose_name='Meta Description')
    is_active = models.BooleanField(default=True, verbose_name='وضعیت')
    register_date = jmodels.jDateField(default=jdatetime.date.today(), verbose_name='تاریخ ساخت')
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, related_name='blogs',
                                 verbose_name='دسته بندی')

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقاله ها'

    def __str__(self):
        return self.title


class BlogTag(models.Model):
    tag = models.CharField(max_length=300, verbose_name='تگ')
    is_active = models.BooleanField(default=True, verbose_name='وضعیت')
    register_date = jmodels.jDateField(default=jdatetime.date.today(), verbose_name='تاریخ ساخت')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='tags', verbose_name='مقاله')

    class Meta:
        verbose_name = 'تگ'
        verbose_name_plural = 'تگ ها'

    def __str__(self):
        return self.tag
