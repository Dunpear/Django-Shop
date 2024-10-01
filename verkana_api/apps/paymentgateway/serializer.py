from rest_framework import serializers
from apps.invoice.models import Invoice
from .models import SellerTransaction


class RegisterSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Invoice
        fields = ['id', 'received_phone', 'received_full_name', 'postal_code', 'invoice_description',
                  'ref_id', 'authority']


class RequestMoneySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = SellerTransaction
        fields = ['id', 'mony_request']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerTransaction
        fields = '__all__'
