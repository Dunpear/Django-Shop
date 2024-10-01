from django.db import models
from django_jalali.db import models as jmodels
import jdatetime
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from apps.account.models import CustomerUser
from django.utils.html import mark_safe


# region Brand
class Brand(models.Model):
    brand_title = models.CharField(unique=True, max_length=100, verbose_name='عنوان برند')
    brand_description = models.TextField(null=True, blank=True, verbose_name='توضیحات برند')
    brand_image = models.ImageField(upload_to='products/brands/', verbose_name='لوگو')
    brand_image_alt = models.CharField(max_length=100, null=True, blank=True, verbose_name='متن جایگزین لوگو')
    brand_image_title = models.CharField(max_length=100, null=True, blank=True, verbose_name='عنوان لوگو')
    width = models.IntegerField(null=True, blank=True, verbose_name='عرض تصویر')
    height = models.IntegerField(null=True, blank=True, verbose_name='ارتفاع تصوبر')
    css_class = models.CharField(max_length=500, null=True, blank=True, verbose_name='کلاس اضافی')
    css_style = models.CharField(max_length=1500, null=True, blank=True, verbose_name='استایل اضافی')
    meta_description = models.TextField(null=True, blank=True, verbose_name='توضیحات متا')
    meta_keywords = models.CharField(max_length=500, null=True, blank=True, verbose_name='کلمات کلیدی')
    slug = models.SlugField(unique=True, verbose_name='slug')
    is_active = models.BooleanField(default=True, verbose_name='وضعیت')
    register_date = jmodels.jDateField(default=jdatetime.date.today(), verbose_name='تاریخ ساخت')

    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برند ها'

    def __str__(self):
        return self.brand_title

    def get_brand_img(self):
        return mark_safe(
            '<img src="/media/%s" width="50" height="50" style="border-radius:5px;" />' % (self.brand_image))

    get_brand_img.short_description = 'تصویر برند'
    get_brand_img.allow_tags = True


# endregion

# region Product Group
class ProductGroup(models.Model):
    group_title = models.CharField(max_length=100, verbose_name='عنوان گروه کالا')
    group_image = models.ImageField(upload_to='products/groups/', blank=True, null=True, verbose_name='لوگو دسته بندی')
    group_image_alt = models.CharField(max_length=100, null=True, blank=True, verbose_name='متن جایگزین لوگو')
    group_image_title = models.CharField(max_length=100, null=True, blank=True, verbose_name='عنوان لوگو')
    width = models.IntegerField(null=True, blank=True, verbose_name='عرض تصویر')
    height = models.IntegerField(null=True, blank=True, verbose_name='ارتفاع تصوبر')
    css_class = models.CharField(max_length=500, null=True, blank=True, verbose_name='کلاس اضافی')
    css_style = models.CharField(max_length=1500, null=True, blank=True, verbose_name='استایل اضافی')
    description = RichTextField(config_name='special', null=True, blank=True, verbose_name='توضیحات گروه کالا')
    meta_description = models.TextField(null=True, blank=True, verbose_name='توضیحات متا')
    meta_keywords = models.CharField(max_length=500, null=True, blank=True, verbose_name='کلمات کلیدی')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیر فعال')
    register_date = jmodels.jDateField(default=jdatetime.date.today(), verbose_name='تاریخ ساخت')
    slug = models.SlugField(max_length=200, verbose_name='slug')
    group_parent = models.ForeignKey('ProductGroup', on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='groups', verbose_name='والد گروه کالا')

    def __str__(self):
        return self.group_title

    class Meta:
        verbose_name = 'گروه محصول'
        verbose_name_plural = 'گروه محصولات'


# endregion

# region Group Feature
class Feature(models.Model):
    feature_title = models.CharField(max_length=100, verbose_name='عنوان ویژگی')
    product_group = models.ForeignKey(ProductGroup, verbose_name='گروه کالا', related_name='category_features',
                                       on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True, verbose_name='وضعیت')

    def __str__(self):
        return self.feature_title

    class Meta:
        verbose_name = 'ویژگی گروه محصول'
        verbose_name_plural = 'ویژگی های گروه محصولات'


# endregion

# region Product
class Product(models.Model):
    product_name = models.CharField(max_length=200, verbose_name='نام کالا')
    short_description = RichTextField(config_name='special', verbose_name='توضیحات مختصر کالا')
    full_description = RichTextUploadingField(config_name='special', verbose_name='توضیحات کامل کالا')
    cover_picture = models.ImageField(upload_to='products/cover/', verbose_name='تصویر اصلی کالا')
    group_image_alt = models.CharField(max_length=100, null=True, blank=True, verbose_name='متن جایگزین کاور')
    group_image_title = models.CharField(max_length=100, null=True, blank=True, verbose_name='عنوان کاور')
    width = models.IntegerField(null=True, blank=True, verbose_name='عرض کاور')
    height = models.IntegerField(null=True, blank=True, verbose_name='ارتفاع کاور')
    css_class = models.CharField(max_length=500, null=True, blank=True, verbose_name='کلاس اضافی')
    css_style = models.CharField(max_length=1500, null=True, blank=True, verbose_name='استایل اضافی')
    purchase_price = models.IntegerField(verbose_name='قیمت خرید', default=0)
    sell_price = models.IntegerField(verbose_name='قیمت فروش', default=0)
    product_discount = models.IntegerField(default=0, verbose_name='تخفیف')
    product_after_discount = models.IntegerField(default=0, null=True, blank=True, verbose_name='قیمت پس از تخفیف')
    slug = models.SlugField(max_length=200, verbose_name='slug', unique=True, allow_unicode=True,
                            db_collation='utf8_persian_ci')
    is_mixin = models.BooleanField(default=False, verbose_name='فروش این محصول به عنوان ترکیب')
    exist_count = models.IntegerField(default=0, verbose_name='تعداد محصول')
    product_view_count = models.IntegerField(default=0, verbose_name='تعداد بازدید')
    product_sell_count = models.IntegerField(default=0, verbose_name='تعداد فروش')
    is_active = models.BooleanField(default=True, blank=True, verbose_name='فعال / غیر فعال')
    is_deleted = models.BooleanField(default=False, verbose_name='حذف / نمایش')
    register_date = jmodels.jDateField(default=jdatetime.date.today(), verbose_name='تاریخ درج')
    updated_date = jmodels.jDateField(default=jdatetime.date.today(), verbose_name='تاریخ آخرین بروزرسانی')


    user = models.ForeignKey(CustomerUser, default=None, blank=True, null=True, related_name='products',
                             on_delete=models.CASCADE,
                             verbose_name='فروشنده')
    product_group = models.ManyToManyField(ProductGroup, verbose_name='گروه کالا', related_name='products_of_groups')
    brand = models.ForeignKey(Brand, verbose_name='برند کالا', null=True, on_delete=models.CASCADE,
                              related_name='brands')
    features = models.ManyToManyField(Feature, through='ProductFeature')

    # def save(self, *args, **kwargs):
    #     self.product_after_discount = self.sell_price - ((self.sell_price * self.product_discount) / 100)
    #     super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    # Todo: باید قیمت پس از تخفیف رو توی تابع ذخیره با بازنویسی درست کرد

    def get_cover(self):
        return mark_safe(
            '<img src="/media/%s" width="100" height="100" style="border-radius:10px;" />' % (self.cover_picture))

    get_cover.short_description = 'کاور محصول'
    get_cover.allow_tags = True


class ProductTag(models.Model):
    tag_name = models.CharField(max_length=100, verbose_name='عنوان تگ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='tags', verbose_name='محصول')

    class Meta:
        verbose_name = 'تگ محصول'
        verbose_name_plural = 'تگهای محصول'

    def __str__(self):
        return self.tag_name


# endregion

# region Product Feature
class ProductFeature(models.Model):
    feature_value = models.CharField(max_length=150, verbose_name='مقدار ویژگی')
    is_active = models.BooleanField(default=True, blank=True, verbose_name='فعال / غیر فعال')

    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name='product_features',
                                verbose_name='کالا',
                                )
    feature = models.ForeignKey(to=Feature, on_delete=models.CASCADE, related_name='group_features',
                                verbose_name='ویژگی', )

    def __str__(self):
        return f'{self.product} - {self.feature} : {self.feature_value}'

    class Meta:
        verbose_name = 'ویژگی محصول'
        verbose_name_plural = 'ویژگی های محصولات'


# endregion

# region Product Gallery
class ProductGallery(models.Model):
    product_picture = models.ImageField(upload_to='products/galleries/', verbose_name='تصویر')
    product_picture_alt = models.CharField(max_length=100, null=True, blank=True, verbose_name='متن جایگزین تصویر')
    product_picture_title = models.CharField(max_length=100, null=True, blank=True, verbose_name='عنوان تصویر')
    width = models.IntegerField(null=True, blank=True, verbose_name='عرض تصویر')
    height = models.IntegerField(null=True, blank=True, verbose_name='ارتفاع تصویر')
    css_class = models.CharField(max_length=500, null=True, blank=True, verbose_name='کلاس اضافی')
    css_style = models.CharField(max_length=1500, null=True, blank=True, verbose_name='استایل اضافی')
    is_active = models.BooleanField(default=True, blank=True, verbose_name='فعال / غیر فعال')
    product = models.ForeignKey(Product, related_name='product_gallery', on_delete=models.CASCADE, verbose_name='کالا')

    class Meta:
        verbose_name = ' گالری محصول'
        verbose_name_plural = 'گالری محصولات'
# endregion
