from django.contrib import admin
from .models import Banner


def active_slider(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    message = f'تعداد {res} بنر فعال شد'
    modeladmin.message_user(request, message)


def de_active_slider(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    message = f'تعداد {res} بنر غیرفعال شد'
    modeladmin.message_user(request, message)


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'picture_alt', 'picture_title', 'link', 'link_title', 'is_active')
    actions = [active_slider, de_active_slider]
    ordering = ('-is_active', 'title', 'link', 'link_title')
    search_fields = ('title', 'link')
    list_filter = ('is_active', 'link')

    de_active_slider.short_description = 'غیرفعال سازی بنرهای انتخابی'
    active_slider.short_description = 'فعال سازی بنرهای انتخابی'
