from django.contrib import admin
from .models import Invoice, InvoiceItem, InvoiceLog, MixedItem, Mixed


# region Invoice
class InvoiceItemInstanceAdminInline(admin.TabularInline):
    model = InvoiceItem


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'tax_amount', 'payable_amount', 'invoice_status', 'user', 'received_phone', 'received_full_name',
        'is_pay', 'tracking_code', 'register_date', 'is_returned', 'get_item')
    list_filter = ('is_pay', 'is_returned')
    list_editable = ['invoice_status', ]
    readonly_fields = ('get_item',)
    search_fields = ('received_full_name', 'tracking_code')
    ordering = ('-register_date', 'is_pay', 'is_returned',)
    inlines = [InvoiceItemInstanceAdminInline]


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'invoice', 'get_cover', 'product', 'get_price', 'get_seller', 'count')
    readonly_fields = ('get_cover', 'get_price', 'get_seller')




# endregion


# region Mixing

@admin.register(MixedItem)
class MixedItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'count', 'product', 'total_price')


@admin.register(Mixed)
class MixedAdmin(admin.ModelAdmin):
    list_display = ('id', 'total_price')

# endregion