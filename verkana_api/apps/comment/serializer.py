from rest_framework import serializers
from .models import ProductComment
from apps.account.models import CustomerUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = ['id', 'name', 'family', 'image']


class ProductCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, many=False)

    class Meta:
        model = ProductComment
        fields = ['user', 'comment', 'rate', 'admin_answer', 'register_date', 'is_active']


class SubmitCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductComment
        fields = ['comment', 'product', 'rate']
