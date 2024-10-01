from rest_framework import serializers
from .models import Invoice, InvoiceItem, InvoiceLog, MixedItem, Mixed
from apps.account.serializer import UserForFactorSerializer
from apps.product.serializer import ProductForInvoiceSerializer, ProductSerializer


# region Mix Item serializer

class MixItemSerializer(serializers.ModelSerializer):
    product = ProductForInvoiceSerializer(read_only=True, many=False)

    class Meta:
        model = MixedItem
        fields = ['id', 'product', 'count', 'total_price']

# endregion


# region Mixed Serializer

class InvoiceItemForMixSerializer(serializers.ModelSerializer):
    product = ProductForInvoiceSerializer(read_only=True, many=False)

    class Meta:
        model = InvoiceItem
        fields = ('id', 'invoice', 'count', 'product')

class InvoiceForMixSerializer(serializers.ModelSerializer):
    user = UserForFactorSerializer(read_only=True, many=False)

    invoice_items = InvoiceItemForMixSerializer(read_only=True, many=True)

    class Meta:
        model = Invoice
        fields = (
            'id', 'tax_amount', 'payable_amount', 'receiver_address', 'received_phone', 'received_full_name',
            'postal_code', 'invoice_description', 'is_pay', 'ref_id', 'authority', 'tracking_code', 'register_date',
            'delivery_date', 'is_returned', 'returned_date', 'invoice_status',
            'user', 'invoice_items', 'mixed_item')


class MixedSerializer(serializers.ModelSerializer):
    mix_items = MixItemSerializer(read_only=True, many=True)
    invoice = InvoiceForMixSerializer(read_only=True, many=False)

    class Meta:
        model = Mixed
        fields = ['id', 'total_price', 'mix_items', 'invoice']

# endregion


# region Mix Item Crud Serializer

class UpdateItemMixSerializer(serializers.Serializer):
    mix_item = serializers.IntegerField()
    count = serializers.IntegerField()

class AddItemMixSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    count = serializers.IntegerField()


class AddMixedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mixed
        fields = ['mix_items']


class GetMixedSerializer(serializers.Serializer):
    mixed_id = serializers.IntegerField()


class GetMixItemSerializer(serializers.Serializer):
    mix_item_id = serializers.IntegerField()


# endregion


# region Invoice and Invoice Item


class InvoiceItemSerializer(serializers.ModelSerializer):
    product = ProductForInvoiceSerializer(read_only=True, many=False)

    class Meta:
        model = InvoiceItem
        fields = ('id', 'invoice', 'count', 'product')


class InvoiceItemForAddSerializer(serializers.ModelSerializer):
    product = ProductForInvoiceSerializer(read_only=True)

    class Meta:
        model = InvoiceItem
        fields = ['count', 'product']


class InvoiceSerializer(serializers.ModelSerializer):
    user = UserForFactorSerializer(read_only=True, many=False)

    invoice_items = InvoiceItemSerializer(read_only=True, many=True)
    mixed_item = MixedSerializer(read_only=True, many=True)

    class Meta:
        model = Invoice
        fields = (
            'id', 'tax_amount', 'payable_amount', 'receiver_address', 'received_phone', 'received_full_name',
            'postal_code', 'invoice_description', 'is_pay', 'ref_id', 'authority', 'tracking_code', 'register_date',
            'delivery_date', 'is_returned', 'returned_date', 'invoice_status',
            'user', 'invoice_items', 'mixed_item')


class ChangeInvoiceStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['invoice_status']


class AddInvoiceSerializer(serializers.ModelSerializer):
    user = UserForFactorSerializer(read_only=True, many=False)
    qty = serializers.IntegerField()
    product_id = serializers.IntegerField()

    class Meta:
        model = Invoice
        fields = ['user', 'product_id', 'qty']



# endregion


# region Update Invoice Item

class UpdateInvoiceItemSerializer(serializers.Serializer):
    qty = serializers.IntegerField()


# endregion


# region Update Invoice Information

class UpdateInvoiceInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['receiver_address', 'received_phone', 'received_full_name']

# endregion