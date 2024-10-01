from rest_framework import serializers
from .models import CustomerUser
from apps.comment.serializer import ProductComment


class ProductCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductComment
        fields = ['user', 'comment', 'rate', 'admin_answer', 'register_date', 'is_active']


class CustomerUserSerializer(serializers.ModelSerializer):
    def validate_user_phone(self, user_phone):
        if len(user_phone) < 11 and len(user_phone) > 11:
            raise serializers.ValidationError("فرمت ارسالی شماره موبایل اشتباه است")
        elif not user_phone.isnumeric():
            raise serializers.ValidationError("فرمت ارسالی موبایل اشتباه است")
        return user_phone

    def validate_name(self, name):
        if len(name) <= 0:
            raise serializers.ValidationError("وارد کردن نام اجباری است")
        elif len(name) > 50:
            raise serializers.ValidationError('تعداد کاراکتر مجاز 50 می باشد')
        return name

    def validate_family(self, family):
        if len(family) <= 0:
            raise serializers.ValidationError("وارد کردن نام خانوادگی اجباری است")
        elif len(family) > 50:
            raise serializers.ValidationError('تعداد کاراکتر مجاز 50 می باشد')
        return family

    user_comment = ProductCommentSerializer(many=True, read_only=True)

    class Meta:

        model = CustomerUser
        fields = ['user_phone', 'name', 'family', 'gender', 'password', 'user_comment']


class CustomerUserGetInfoSerializer(serializers.ModelSerializer):
    user_comment = ProductCommentSerializer(many=True, read_only=True)

    class Meta:
        model = CustomerUser
        fields = ['user_phone', 'name', 'family', 'gender', 'image', 'user_comment']


class UserForFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = ['name', 'family', 'user_phone', 'id']


class ManageCustomerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = ['name', 'family', 'gender']


class ActiveCustomerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = ['active_code', 'user_phone']


class GetDataActiveCodeSerializer(serializers.Serializer):
    user_phone = serializers.CharField(max_length=11)
    active_code = serializers.CharField()


class RecoveryCustomerUserSerializer(serializers.ModelSerializer):

    def validate_password(self, password):
        if len(password) < 6:
            raise serializers.ValidationError("تعداد کاراکتر کمتر از حد مجاز است . حد مجاز : 6")
        return password

    class Meta:
        model = CustomerUser
        fields = ['user_phone', 'active_code', 'password', ]



class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()

