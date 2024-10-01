from django.contrib import admin
from .models import SellerSelling, SellerTransaction


@admin.register(SellerSelling)
class SellerSellingAdmin(admin.ModelAdmin):
    list_display = ('id', 'total_amount')



@admin.register(SellerTransaction)
class SellerTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'total_sell_amount', 'user')\


