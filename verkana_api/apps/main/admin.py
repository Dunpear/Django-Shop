from django.contrib import admin
from .models import SiteRules, SiteSettings, SocialMedia, RepetitiveQuestions, Advantages


# region Site Rules
def active_rule(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    message = f'تعداد {res} سیاست فعال شد'
    modeladmin.message_user(request, message)


def de_active_rule(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    message = f'تعداد {res} سیات غیرفعال شد'
    modeladmin.message_user(request, message)


@admin.register(SiteRules)
class SiteRulesAdmin(admin.ModelAdmin):
    list_display = ('site_rule_name', 'site_rule_description', 'register_date', 'is_active')
    search_fields = ('site_rule_name',)
    list_filter = ('is_active',)
    actions = [active_rule, de_active_rule]
    ordering = ('register_date', 'is_active', 'site_rule_name',)

    active_rule.short_description = 'فعال سازی سیاست های انتخابی'
    de_active_rule.short_description = 'غیرفعال کردن سیاست های انتخابی'


# endregion

# region Site Settings
def active_site_setting(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    message = f'تعداد {res} تنظیمات فعال شد'
    modeladmin.message_user(request, message)


def de_active_site_setting(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    message = f'تعداد {res} تنظیمات غیرفعال شد'
    modeladmin.message_user(request, message)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_title', 'tel_number', 'logo_alt', 'logo_title', 'register_date', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('site_title',)
    ordering = ('-register_date', 'site_title',)
    actions = [active_site_setting, de_active_site_setting]

    active_site_setting.short_description = 'فعال سازی تنظیم های انتخابی'
    de_active_site_setting.short_description = 'غیرفعال کردن تنظیم های انتخابی'


# endregion

# region Social Media
def active_social_media(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    message = f'تعداد {res} شبکه اجتماعی فعال شد'
    modeladmin.message_user(request, message)


def de_active_social_media(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    message = f'تعداد {res} شبکه اجتماعی غیرفعال شد'
    modeladmin.message_user(request, message)


@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = (
        'social_media_name', 'social_media_url', 'social_media_image_alt', 'social_media_image_title', 'register_date',
        'is_active',)
    search_fields = ('social_media_name', 'social_media_url')
    ordering = ('-register_date', 'social_media_name',)
    actions = [active_social_media, de_active_social_media]
    list_filter = ('is_active',)

    active_social_media.short_description = 'فعال سازی شبکه های اجتماعی انتخابی'
    de_active_social_media.short_description = 'غیرفعال کردن شبکه های اجتماعی انتخابی'


# endregion

# region Repetitive Questions
def active_repetitive_questions(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    message = f'تعداد {res} سوال متداول فعال شد'
    modeladmin.message_user(request, message)


def de_active_repetitive_questions(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    message = f'تعداد {res} سوال متداول غیرفعال شد'
    modeladmin.message_user(request, message)


@admin.register(RepetitiveQuestions)
class RepetitiveQuestionsAdmin(admin.ModelAdmin):
    list_display = ('repetitive_question', 'repetitive_answer', 'register_date', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('repetitive_question', 'repetitive_answer',)
    ordering = ('-register_date', 'repetitive_question',)
    actions = [active_repetitive_questions, de_active_repetitive_questions]

    active_social_media.short_description = 'فعال سازی سوالات متداول انتخابی'
    de_active_social_media.short_description = 'غیرفعال کردن سوالات متداول انتخابی'
# endregion



@admin.register(Advantages)
class AdvantagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'advantage_name','register_date', 'is_active', 'color')
    list_editable = ('advantage_name', 'color', 'is_active',)
    list_filter = ('is_active',)
    search_fields = ('advantage_name',)
    ordering = ('is_active',)
