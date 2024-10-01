import jdatetime
from django.shortcuts import render
from .models import SellerSelling
from rest_framework.views import APIView, Request
from apps.invoice.models import Invoice
from .models import SellerSelling, SellerTransaction
from rest_framework.response import Response
from .serializer import RegisterSerializer, RequestMoneySerializer, TransactionSerializer
from rest_framework import status
from apps import utilities
from drf_spectacular.utils import extend_schema
from apps.account.models import CustomerUser


# region SellerSelling Api View

class RegistrationPayment(APIView):
    @extend_schema(
        request=RegisterSerializer,
    )
    def post(self, request):

        # region validate parametres

        # اطلاعات ارسالی رو چک میکنیم!
        serilize_data = RegisterSerializer(data=request.data)
        if serilize_data.is_valid():
            pass
        else:
            return Response(
                utilities.response_formatter(None, status.HTTP_400_BAD_REQUEST, 'مقادیر لازم به درستی وارد نشده است!'))

        # چک میکنیم فاکتور در سیستم وجود داشته باشه
        try:
            factor = Invoice.objects.get(id=serilize_data.validated_data['id'])
        except Invoice.DoesNotExist:
            return Response(utilities.response_formatter(None, status.HTTP_404_NOT_FOUND, 'فاکتور پیدا نشد!'))

        # endregion

        # region edit factor

        factor.is_pay = True
        factor.received_phone = serilize_data.validated_data['received_phone']
        factor.received_full_name = serilize_data.validated_data['received_full_name']
        factor.postal_code = serilize_data.validated_data['postal_code']
        factor.invoice_description = serilize_data.validated_data['invoice_description']
        factor.ref_id = serilize_data.validated_data['ref_id']
        factor.authority = serilize_data.validated_data['authority']
        factor.invoice_status = '1'
        factor.save()

        # endregion

        # region seller selling
        seller_users = factor.invoice_items.all()  # تمام آیتم های فاکتور رو بیرون میکشیم

        users = {}  # لیست فروشنده ها و کل قیمت قاکتور بر حسب محصولاتشون و تعدادشون

        #  روی ایتم های فاکتور پیمایش میکنیم
        for seller in seller_users:
            # در صورتی که چندتا از محصولات این فاکتور برای یک فروشنده باشه مبلغ رو اپدیت میکنیم
            # '* نکته *' : دیتا شامل ایدی فروشنده و سودش از این فاکتور هست
            if int(seller.product.user.id) in users.keys():
                last_price = users[int(seller.product.user.id)]
                users.update(
                    {int(seller.product.user.id): int(last_price) + int(seller.product.product_after_discount) * int(
                        seller.count)})
            else:
                # در صورتی که فقط یه محصول بود یه دیتا اضافه میکنیم
                users.update(
                    {int(seller.product.user.id): int(seller.product.product_after_discount) * int(seller.count)})

            # لیست کلی محصولات که بالا تعریف کردیم رو پر میکنیم

        # endregion

        # region Transaction
        for key, value in users.items():
            seller_user = CustomerUser.objects.get(id=key)
            new_selling = SellerSelling.objects.create(total_amount=int(value),
                                                       is_calculation=True,
                                                       register_date=jdatetime.date.today(),
                                                       user=seller_user,
                                                       invoice=factor)
            try:
                transaction = SellerTransaction.objects.get(user=seller_user)
            except SellerTransaction.DoesNotExist:
                transaction = None

            if transaction is not None:
                transaction.total_sell_amount += int(value)  # مبلغ کل رو اپدیت میکنیم!
                transaction.commission_percentage = 10  # درصد پورسانت رو اپدیت میکنیم (نیاز به داینامیک سازی )
                transaction.save()  # باید یه بار سیو بکنیم که بتونیم با مبلغ کل جدید درصد پورسانت رو حساب کنیم!
                transaction.commission_amount = int(
                    (transaction.total_sell_amount * transaction.commission_percentage) / 100)
                total_after_commission = transaction.total_sell_amount - int(
                    (transaction.total_sell_amount * transaction.commission_percentage) / 100)
                transaction.remaining_amount = total_after_commission
                transaction.save()
            else:
                transaction = SellerTransaction.objects.create(
                    user=seller_user,
                    total_sell_amount=int(value),
                    commission_percentage=10,  # need dynamic
                    commission_amount=int((int(value) * 10) / 100),
                    remaining_amount=int(value) - int((int(value) * 10) / 100)
                )
        # endregion

        return Response(utilities.response_formatter(None, status.HTTP_200_OK, 'فاکتور با موفقیت ثبت و پرداخت شد!'))


# endregion


# region Request Take Money

class MoneyRequestApiView(APIView):
    @extend_schema(
        request=RequestMoneySerializer,
        responses={200: TransactionSerializer},
    )
    def post(self, request: Request):
        serialize_data = RequestMoneySerializer(data=request.data)

        # region validated data

        if serialize_data.is_valid():
            pass
        else:
            return Response(
                utilities.response_formatter(None, status.HTTP_400_BAD_REQUEST, 'لطفا اطلاعات درخواست را ارسال کنید!'))

        print(serialize_data.validated_data['mony_request'])

        try:
            custumer_seller = CustomerUser.objects.get(id=serialize_data.validated_data['id'])
        except:
            return Response(utilities.response_formatter(None, status.HTTP_404_NOT_FOUND, 'فروشنده پیدا نشد!'))

        try:
            transaction = SellerTransaction.objects.get(user=custumer_seller)
        except SellerTransaction.DoesNotExist:
            return Response(
                utilities.response_formatter(None, status.HTTP_404_NOT_FOUND, 'هنوز هیچ تراکنشی ثبت نشده است!'))

        if transaction.is_money_requested:
            return Response(utilities.response_formatter(None, status.HTTP_429_TOO_MANY_REQUESTS,
                                                         'امکان ثبت درخواست وجه وجود ندارد، یک درخواست در حال انتظار وجود دارد!'))
        elif serialize_data.validated_data['mony_request'] > transaction.remaining_amount:
            return Response(utilities.response_formatter(None, status.HTTP_400_BAD_REQUEST,
                                                         'وجه درخواستی از وجه مانده در حساب بیشتر است!'))

        # endregion

        transaction.is_money_requested = True
        transaction.mony_request = serialize_data.validated_data['mony_request']
        transaction.mony_request_date = jdatetime.date.today()
        transaction.save()

        serialize_response = TransactionSerializer(transaction, many=False).data

        # send sms or email to azimi !

        return Response(
            utilities.response_formatter(serialize_response, status.HTTP_200_OK, 'درخواست وجه با موفقیت ثبت شد!'))


# endregion


class DetailTransactionApiView(APIView):
    def get(self, request: Request, transaction_id):

        try:
            custumer_seller = CustomerUser.objects.get(id=transaction_id)
        except:
            return Response(utilities.response_formatter(None, status.HTTP_404_NOT_FOUND, 'فروشنده پیدا نشد!'))

        try:
            transaction = SellerTransaction.objects.get(user=custumer_seller)
        except SellerTransaction.DoesNotExist:
            return Response(
                utilities.response_formatter(None, status.HTTP_404_NOT_FOUND, 'هنوز هیچ تراکنشی ثبت نشده است!'))

        serialize_transaction = TransactionSerializer(transaction, many=False)
        return Response(
            utilities.response_formatter(serialize_transaction.data, status.HTTP_200_OK, 'اطلاعات مجموع تراکنش'))
