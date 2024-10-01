from django.contrib import admin
from apps.account.models import CustomerUser


def active_customer(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    message = f'تعداد {res} کاربر فعال شد'
    modeladmin.message_user(request, message)


def de_active_customer(modeladmin, request, queryset):
    res = queryset.update(is_active=False)
    message = f'تعداد {res} کاربر غیرفعال شد'
    modeladmin.message_user(request, message)


@admin.register(CustomerUser)
class CustomerUserAdmin(admin.ModelAdmin):
    list_display = ('user_phone', 'name', 'family', 'is_active', 'register_date')
    ordering = ('is_active', 'user_phone')
    search_fields = ('user_phone', 'name', 'family')
    list_filter = ('is_active',)
    verbose_name = 'کاربر'
    verbose_name_plural = 'کاربران'
    actions = [de_active_customer, active_customer]
    de_active_customer.short_description = 'غیرفعال سازی کاربران انتخابی'
    active_customer.short_description = 'فعال سازی کاربران انتخابی'
    filter_horizontal = ('groups', 'user_permissions')
