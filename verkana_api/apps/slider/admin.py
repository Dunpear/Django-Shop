from django.contrib import admin
from .models import Slider, SliderItem
from django.db.models.aggregates import Count


# region SliderItem

def active_slider_item(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    message = f'تعداد {res} اسلایدر فعال شد'
    modeladmin.message_user(request, message)


def de_active_slider_item(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    message = f'تعداد {res} اسلایدر غیرفعال شد'
    modeladmin.message_user(request, message)


@admin.register(SliderItem)
class SliderItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'link_title', 'picture_alt', 'picture_title', 'is_active',)
    search_fields = ('title', 'link',)
    list_filter = ('is_active',)
    actions = [active_slider_item, de_active_slider_item]
    ordering = ['register_date']

    active_slider_item.short_description = 'فعال کردن اسلایدر های انتخابی'
    de_active_slider_item.short_description = 'غیرفعال کردن اسلایدر های انتخابی'


# endregion


# region Slide
def active_slider(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    message = f'تعداد {res} اسلاید فعال شد'
    modeladmin.message_user(request, message)


def de_active_slider(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    message = f'تعداد {res} اسلاید غیرفعال شد'
    modeladmin.message_user(request, message)


# class SlideInstanceAdminInline(admin.TabularInline):
#     model = SliderItem


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'register_date', 'delay', 'auto_play', 'is_active',)
    ordering = ('delay', 'register_date')
    search_fields = ('title',)
    list_filter = ('delay', 'auto_play', 'is_active',)
    actions = [active_slider, de_active_slider]
    # inlines = [SlideInstanceAdminInline]

    active_slider.short_description = 'فعال کردن اسلاید های انتخابی'
    de_active_slider.short_description = 'غیرفعال کردن اسلاید های انتخابی'

# endregion
