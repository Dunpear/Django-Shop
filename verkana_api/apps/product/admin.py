from django.contrib import admin
from django.db.models.aggregates import Count
from .models import (Product, Brand, Feature, ProductFeature,
                     ProductTag, ProductGroup, ProductGallery)


# region Brand
def active_brand(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    message = f'تعداد {res} برند  فعال شد'
    modeladmin.message_user(request, message)


def de_active_brand(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    message = f'تعداد {res}برند  غیرفعال شد'
    modeladmin.message_user(request, message)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = (
        'brand_title', 'get_brand_img', 'brand_image_alt', 'brand_image_title', 'css_class', 'css_style',
        'meta_keywords',
        'register_date',
        'is_active')
    readonly_fields = ('get_brand_img',)
    list_editable = ['meta_keywords']
    actions = [active_brand, de_active_brand]
    search_fields = ['brand_title']
    ordering = ['-register_date', 'brand_title']
    list_filter = ['is_active']
    active_brand.short_description = 'فعال سازی برندهای انتخابی'
    de_active_brand.short_description = 'غیرفعال کردن برندهای انتخابی'


# endregion

# region Product Group
def active_product_group(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    message = f'تعداد {res} گروه محصول  فعال شد'
    modeladmin.message_user(request, message)


def de_active_product_group(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    message = f'تعداد {res}گروه محصول  غیرفعال شد'
    modeladmin.message_user(request, message)


class FeatureInstanceAdminInline(admin.TabularInline):
    model = Feature


@admin.register(ProductGroup)
class ProductGroupAdmin(admin.ModelAdmin):
    list_display = (
        'group_title', 'group_image_alt', 'group_parent', 'group_image_title', 'meta_keywords',
        'register_date', 'slug', 'count_sub_group', 'count_product_of_group', 'is_active')
    list_filter = ('is_active',)
    list_editable = ['meta_keywords', ]
    search_fields = ('group_title',)
    actions = [active_product_group, de_active_product_group]
    ordering = ('-register_date', 'group_title',)
    inlines = [FeatureInstanceAdminInline]
    prepopulated_fields = {"slug": ("group_title",)}

    # اضافه کردن فیلد به جدول
    def get_queryset(self, *args, **kwargs):
        qs = super(ProductGroupAdmin, self).get_queryset(*args, **kwargs)
        qs = qs.annotate(sub_group=Count('groups'))
        qs = qs.annotate(product_of_group=Count('products_of_groups'))
        return qs

    def count_product_of_group(self, obj):
        return obj.product_of_group

        # اضافه کردن فیلد به جدول

    def count_sub_group(self, obj):
        return obj.sub_group

    count_sub_group.short_description = 'تعداد زیر گروه'
    de_active_product_group.short_description = 'غیرفعال سازی گروه های انتخابی'
    active_product_group.short_description = 'فعال سازی گروه های انتخابی'
    count_product_of_group.short_description = 'تعداد کالا در گروه'


# endregion

# region Group Feature

def active_feature(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    message = f'تعداد {res}ویژگی گروه  فعال شد'
    modeladmin.message_user(request, message)


def de_active_feature(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    message = f'تعداد {res}ویژگی گروه  غیرفعال شد'
    modeladmin.message_user(request, message)


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('product_group', 'feature_title', 'is_active')
    list_filter = ('is_active',)
    list_editable = ['feature_title']
    search_fields = ('feature_title',)
    ordering = ('feature_title', 'is_active',)
    actions = [active_feature, de_active_feature]

    de_active_feature.short_description = 'غیرفعال سازی ویژگی های انتخابی'
    active_feature.short_description = 'فعال سازی ویژگی های انتخابی'


# endregion

# region Product
def de_active_product(modeladmin, request, queryset):  # برای اضافه کردن اکشن
    res = queryset.update(is_active=False)
    message = f'تعداد {res} کالا غیر فعال شد '
    modeladmin.message_user(request, message)


def active_product(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    message = f'تعداد {res} کالا  فعال شد '
    modeladmin.message_user(request, message)


class ProductFeatureInstanceAdminInline(admin.TabularInline):
    model = ProductFeature


class ProductTagInstanceAdminInline(admin.TabularInline):
    model = ProductTag


class ProductGalleryStackedInline(admin.StackedInline):
    model = ProductGallery


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'product_name','id', 'get_cover', 'purchase_price', 'sell_price', 'product_discount', 'product_after_discount',
        'display_product_groups', 'exist_count', 'product_view_count', 'product_sell_count', 'is_active',
        'register_date', 'updated_date')
    readonly_fields = ('get_cover',)
    editable_fields = ['is_active', 'is_deleted', 'purchase_price', 'sell_price', 'product_discount', ]
    search_fields = ('product_name', 'sell_price')
    list_filter = ('is_active', 'is_deleted')
    ordering = ('-register_date', 'sell_price', 'purchase_price', 'product_discount', 'updated_date',)
    actions = [de_active_product, active_product]

    inlines = [ProductFeatureInstanceAdminInline, ProductTagInstanceAdminInline, ProductGalleryStackedInline]

    de_active_product.short_description = 'غیرفعال سازی کالا های انتخابی'
    active_product.short_description = 'فعال سازی کالا های انتخابی'

    def display_product_groups(self, obj):
        return '- '.join([group.group_title for group in obj.product_group.all()])

    display_product_groups.short_description = 'گروه محصول'


# endregion

# region Product Tag
@admin.register(ProductTag)
class ProductTagAdmin(admin.ModelAdmin):
    list_display = ('product', 'tag_name',)
    list_editable = ['tag_name']
    search_fields = ('tag_name',)
    ordering = ('tag_name', 'product')


# endregion

# region Product Feature
def active_product_feature(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    message = f'تعداد {res} ویژگی محصول  فعال شد'
    modeladmin.message_user(request, message)


def de_active_product_feature(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    message = f'تعداد {res}ویژگی محصول  غیرفعال شد'
    modeladmin.message_user(request, message)


@admin.register(ProductFeature)
class ProductFeatureAdmin(admin.ModelAdmin):
    list_display = ('product', 'feature', 'feature_value', 'is_active',)
    list_editable = ['feature_value']
    ordering = ('feature', 'product', 'feature_value')
    actions = [de_active_product_feature, active_product_feature]
    search_fields = ('feature_value',)

    active_product_feature.short_description = 'فعال سازی ویژگی های محصول انتخابی'
    de_active_product_feature.short_description = 'غیرفعال کردن ویژگی های محصول انتخابی'


# endregion

# region Product Gallery
def de_active_product_gallery(modeladmin, request, queryset):  # برای اضافه کردن اکشن
    res = queryset.update(is_active=False)
    message = f'تعداد {res} عکس از گالری غیر فعال شد '
    modeladmin.message_user(request, message)


def active_product_gallery(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    message = f'تعداد {res} عکس از گالری  فعال شد '
    modeladmin.message_user(request, message)


@admin.register(ProductGallery)
class ProductGalleryAdmin(admin.ModelAdmin):
    list_display = ('product', 'product_picture', 'product_picture_alt', 'product_picture_title', 'is_active')
    actions = [de_active_product_gallery, active_product_gallery]
    list_editable = ['is_active', 'product_picture_alt', 'product_picture_title']

    active_product_gallery.short_description = 'فعال سازی عکس از گالری محصول انتخابی'
    de_active_product_gallery.short_description = 'غیرفعال کردن عکس از گالری محصول انتخابی'

# endregion
