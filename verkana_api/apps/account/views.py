from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema

from apps.account.serializer import (CustomerUserSerializer, ManageCustomerUserSerializer, ActiveCustomerUserSerializer,
                                     RecoveryCustomerUserSerializer, CustomerUserGetInfoSerializer,
                                     ChangePasswordSerializer, GetDataActiveCodeSerializer)
from .models import CustomerUser
from apps import utilities

from apps.permissions import CheckPermission

from rest_framework_simplejwt.authentication import *


class CustomerUserManager(APIView):
    @extend_schema(
        request=CustomerUserSerializer,
        responses={200: CustomerUserSerializer},
    )
    def post(self, request: Request):
        customer_user = CustomerUserSerializer(data=request.data)
        if customer_user.is_valid():
            active_code = utilities.generate_code(6)
            costumer = CustomerUser.objects.create_user(user_phone=customer_user.data['user_phone'],
                                                        name=customer_user.data['name'],
                                                        family=customer_user.data['family'],
                                                        active_code=active_code, gender=customer_user.data['gender'],
                                                        password=customer_user.data['password'])

            # TODO : send active code to user by sms
            return Response(utilities.response_formatter(None, status.HTTP_200_OK, 'ثبت نام با موفقیت انجام شد'))
        else:
            check_error = CustomerUser.objects.filter(user_phone=customer_user.data['user_phone'])
            if check_error:
                if check_error.first().is_active == False:
                    return Response(
                        utilities.response_formatter(None, status.HTTP_200_OK, 'ثبت نام با موفقیت انجام شد'))
                return Response(
                    utilities.response_formatter(None, status.HTTP_400_BAD_REQUEST,
                                                 'این شماره موبایل قبلا ثبت شده است!'))
            return Response(
                utilities.response_formatter(None, status.HTTP_400_BAD_REQUEST, 'فیلدها را اشتباه وارد کرده اید'))


class CustomerUserDetailViewSet(APIView):
    def get_user(self, user_phone: str):
        try:
            customer = CustomerUser.objects.get(user_phone=user_phone)
            return customer
        except CustomerUser.DoesNotExist:
            return None

    @extend_schema(
        request=CustomerUserSerializer,
        responses={200: CustomerUserGetInfoSerializer},
    )
    def get(self, request: Request):
        permission_classes = [IsAuthenticated, CheckPermission]
        authentication_classes = JWTAuthentication

        user = self.get_user(request.user.user_phone)
        if user is None:
            return Response(
                utilities.response_formatter(None, status.HTTP_404_NOT_FOUND, 'کاربری با این شماره یافت نشد'))
        serializer = CustomerUserGetInfoSerializer(user, many=False)
        return Response(utilities.response_formatter(serializer.data, status.HTTP_200_OK, ''))

    @extend_schema(
        request=ManageCustomerUserSerializer,
        responses={200: ManageCustomerUserSerializer},
    )
    def put(self, request: Request):
        permission_classes = [IsAuthenticated, CheckPermission]
        authentication_classes = JWTAuthentication
        user = self.get_user(request.user.user_phone)
        if user is None:
            return Response(
                utilities.response_formatter(None, status.HTTP_404_NOT_FOUND, 'کاربری با این شماره یافت نشد'))
        else:
            user_serialize = ManageCustomerUserSerializer(user, data=request.data)
            if user_serialize.is_valid():
                user_serialize.save()
                return Response(utilities.response_formatter(user_serialize.data, status.HTTP_200_OK,
                                                             'کاربر با موفقیت بروزرسانی شد'))
            else:
                return Response(
                    utilities.response_formatter(None, status.HTTP_400_BAD_REQUEST, 'اطلاعات ارسالی معتبر نیست'))


class CustomerUserActiveAccountApiView(APIView):

    def get_user(self, user_phone: str):
        try:
            customer = CustomerUser.objects.get(user_phone=user_phone)
            return customer
        except CustomerUser.DoesNotExist:
            return None

    @extend_schema(
        request=GetDataActiveCodeSerializer,
        responses={200: ActiveCustomerUserSerializer},
    )
    def post(self, request: Request):
        user_serializer = GetDataActiveCodeSerializer(data=request.data)
        if user_serializer.is_valid():
            try:
                customer_user = CustomerUser.objects.get(user_phone=user_serializer.data['user_phone'])
                if customer_user.is_active:
                    return Response(
                        utilities.response_formatter(None, status.HTTP_400_BAD_REQUEST,
                                                     'حساب کاربری فعال است و نیازی به فعال سازی دوباره نیست!'))
                if user_serializer.data['active_code'] == customer_user.active_code:
                    customer_user.is_active = True
                    customer_user.active_code = utilities.generate_code(6)
                    customer_user.save()
                    return Response(
                        utilities.response_formatter(None, status.HTTP_200_OK, 'حساب کاربری با موفقیت فعال شد'))
                else:
                    return Response(
                        utilities.response_formatter(None, status.HTTP_400_BAD_REQUEST,
                                                     'کد تایید اشتباه وارد شده است!'))
            except CustomerUser.DoesNotExist:
                return Response(
                    utilities.response_formatter(None, status.HTTP_404_NOT_FOUND, 'کاربر با این شماره یافت نشد'))
        else:
            return Response(
                utilities.response_formatter(None, status.HTTP_400_BAD_REQUEST, 'اطلاعات ارسالی صحیح نیست.'))


class RecoveryCustomerUserApiView(APIView):
    def get_user(self, user_phone: str):
        try:
            customer = CustomerUser.objects.get(user_phone=user_phone)
            return customer
        except CustomerUser.DoesNotExist:
            return None

    @extend_schema(
        request=RecoveryCustomerUserSerializer,
        responses={200: RecoveryCustomerUserSerializer},
    )
    def post(self, request: Request):
        user = self.get_user(request.data.get('user_phone'))
        if user is None:
            return Response(
                utilities.response_formatter(None, status.HTTP_404_NOT_FOUND, 'کاربری با این شماره یافت نشد'))
        else:
            user_serialize = RecoveryCustomerUserSerializer(user, data=request.data)
            if user_serialize.is_valid():
                if not user.is_active:
                    return Response(
                        utilities.response_formatter(None, status.HTTP_403_FORBIDDEN,
                                                     'حساب کاربری شما مسدود می باشد. با مدیریت سایت تماس بگیرید'))
                active_code = user.active_code
                # TODO: Send Active Code to User Phone
                return Response(utilities.response_formatter(user_serialize.data, status.HTTP_200_OK,
                                                             'کد تایید به گوشی شما ارسال گردید'))

    @extend_schema(
        request=RecoveryCustomerUserSerializer,
        responses={200: RecoveryCustomerUserSerializer},
    )
    def put(self, request: Request):
        user = self.get_user(request.data.get('user_phone'))
        if user is None:
            return Response(
                utilities.response_formatter(None, status.HTTP_404_NOT_FOUND, 'کاربری با این شماره یافت نشد'))
        else:
            user_serialize = RecoveryCustomerUserSerializer(user, data=request.data)
            if user_serialize.is_valid():
                if user.active_code == user_serialize.data['active_code']:
                    user.set_password(user_serialize.data['password'])
                    user.active_code = utilities.generate_code(6)
                    user.save()
                    return Response(
                        utilities.response_formatter(None, status.HTTP_200_OK,
                                                     'کلمه عبور با موفقیت تغییر کرد'))
                else:
                    return Response(
                        utilities.response_formatter(None, status.HTTP_404_NOT_FOUND,
                                                     'کد ارسالی اشتباه می باشد'))


class CheckAuthToken(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return Response(utilities.response_formatter(
                True, status.HTTP_200_OK, 'authenticated'
            ))
        else:
            return Response(utilities.response_formatter(
                False, status.HTTP_200_OK, 'unauthenticated'
            ))


class ChangePasswordApiView(APIView):
    @extend_schema(
        request=ChangePasswordSerializer,
        responses={200: CustomerUserGetInfoSerializer},
    )
    def post(self, request):
        permission_classes = [IsAuthenticated, CheckPermission]
        authentication_classes = JWTAuthentication

        serializer = ChangePasswordSerializer(data=request.data)

        try:
            user = CustomerUser.objects.get(id=request.user.id)
        except:
            return Response(utilities.response_formatter(None, status.HTTP_400_BAD_REQUEST,
                                                         'کاربر احراز هویت نشده است!'))

        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            if user.check_password(old_password):
                if len(new_password) < 6:
                    return Response(utilities.response_formatter(None, status.HTTP_400_BAD_REQUEST,
                                                                 'طول رمز عبور باید بیشتر از 6 رقم باشد!'))
                else:
                    user.set_password(new_password)
                    user.save()
                    serialize = CustomerUserGetInfoSerializer(user, many=False)
                    return Response(utilities.response_formatter(serialize.data, status.HTTP_200_OK,
                                                                 'رمز عبور با موفقیت تغییر کرد!'))  # success

            else:
                return Response(utilities.response_formatter(None, status.HTTP_400_BAD_REQUEST,
                                                             'رمز عبور فعلی وارد شده اشتباه است!'))
        else:
            return Response(utilities.response_formatter(None, status.HTTP_400_BAD_REQUEST,
                                                         'مقادیر به درستی وارد نشده است!'))


