from django.contrib import admin
from .models import Blog, BlogTag, BlogCategory


# region Blog Category
def active_blog_category(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    message = f'تعداد {res} دسته بندی مقاله فعال شد'
    modeladmin.message_user(request, message)


def de_active_blog_category(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    message = f'تعداد {res} دسته بندی مقاله غیرفعال شد'
    modeladmin.message_user(request, message)


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'register_date', 'picture_alt', 'picture_title', 'is_active')
    search_fields = ('title', 'slug')
    ordering = ('-register_date', 'title', 'is_active')
    actions = [active_blog_category, de_active_blog_category]
    list_filter = ('is_active',)

    active_blog_category.short_description = 'فعال کردن دسته بندی های انتخابی'
    de_active_blog_category.short_description = 'غیرفعال کردن دسته بندی های انتخابی'


# endregion

# region blog
def active_blog(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    message = f'تعداد {res} مقاله فعال شد'
    modeladmin.message_user(request, message)


def de_active_blog(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    message = f'تعداد {res} مقاله غیرفعال شد'
    modeladmin.message_user(request, message)


class BlogTagInstanceAdminInline(admin.TabularInline):
    model = BlogTag


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'picture_alt', 'picture_title', 'meta_keyword', 'register_date', 'is_active', 'category')
    list_filter = ('is_active', 'category')
    ordering = ('-register_date', 'title')
    search_fields = ('title',)
    actions = [active_blog, de_active_blog]
    inlines = [BlogTagInstanceAdminInline]

    active_blog.short_description = 'فعال کردن مقاله های انتخابی'
    de_active_blog.short_description = 'غیرفعال کردن مقاله های انتخابی'


# endregion

# region blog tag
def active_blog_tag(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    message = f'تعداد {res} تگ فعال شد'
    modeladmin.message_user(request, message)


def de_active_blog_tag(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    message = f'تعداد {res} تگ غیرفعال شد'
    modeladmin.message_user(request, message)


@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ('tag', 'register_date', 'is_active', 'blog')
    list_filter = ('is_active', 'blog')
    ordering = ('-register_date', 'tag')
    search_fields = ('tag',)
    actions = [active_blog_tag, de_active_blog_tag]

    active_blog_tag.short_description = 'فعال کردن تگ های انتخابی'
    de_active_blog_tag.short_description = 'غیرفعال کردن تگ های انتخابی'
# endregion
