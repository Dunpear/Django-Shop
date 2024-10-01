from django.contrib import admin
from .models import ProductComment


def active_comment(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    message = f'تعداد {res} نظر فعال شد'
    modeladmin.message_user(request, message)


def de_active_comment(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    message = f'تعداد {res} نظر غیرفعال شد'
    modeladmin.message_user(request, message)


@admin.register(ProductComment)
class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rate', 'comment', 'admin_answer', 'register_date', 'is_active')
    list_editable = ['is_active', 'admin_answer']
    ordering = ('-register_date',)
    list_filter = ['is_active', ]
    actions = [active_comment, de_active_comment]
    active_comment.short_description = 'فعال کردن نظرات انتخابی'
    de_active_comment.short_description = 'غیرفعال کردن نظرات انتخابی'
