from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework import status, permissions
from apps import utilities
from .serializer import (
    InvoiceSerializer, InvoiceItemSerializer, ChangeInvoiceStatusSerializer, AddInvoiceSerializer, MixItemSerializer,
    AddItemMixSerializer, MixedSerializer, AddMixedSerializer, UpdateItemMixSerializer, GetMixedSerializer,
    GetMixItemSerializer, UpdateInvoiceItemSerializer, UpdateInvoiceInformationSerializer)
from .models import Invoice, InvoiceItem, InvoiceLog, MixedItem, Mixed
from apps.product.models import Product
from apps.account.models import CustomerUser

from apps.permissions import CheckPermission
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import *


# region Get Current Invoice

class GetCurrentInvoiceApiView(APIView):
    def get(self, request: Request):
        permission_classes = [IsAuthenticated, CheckPermission]
        authentication_classes = JWTAuthentication

        user = request.user

        if request.user.is_authenticated:

            try:
                invoice = Invoice.objects.get(user=user, is_pay=False, is_returned=False)
            except:
                return Response(utilities.response_formatter(None, status.HTTP_404_NOT_FOUND, 'سبد خریدی وجود ندارد!'))

            serializer = InvoiceSerializer(invoice, many=False)
            return Response(utilities.response_formatter(serializer.data, status.HTTP_200_OK, 'اطلاعات سبد خرید جاری'))
        else:
            return Response(
                utilities.response_formatter(None, status.HTTP_403_FORBIDDEN, 'برای دیدن سبد خرید ابتدا وارد شوید!'))


# endregion

# region Get Invoice
def get_invoice(invoice_id: int):
    try:
        invoices = Invoice.objects.get(id=invoice_id)
        return invoices

    except Invoice.DoesNotExist:
        return None


class GetInvoiceApiView(APIView):
    @extend_schema(
        request=InvoiceSerializer,
        responses={200: InvoiceSerializer},
    )
    def get(self, request: Request, invoice_id: int):
        permission_classes = [IsAuthenticated, CheckPermission]
        authentication_classes = JWTAuthentication

        try:
            invoices = Invoice.objects.get(id=invoice_id)
            if invoices:
                serializer = InvoiceSerializer(invoices, many=False)
                return Response(utilities.response_formatter(serializer.data, status.HTTP_200_OK, 'لیست فاکتور ها'))
            else:
                return Response(utilities.response_formatter(None, status.HTTP_404_NOT_FOUND, 'فاکتور یافت نشد'))
        except Invoice.DoesNotExist:
            return Response(utilities.response_formatter(None, status.HTTP_404_NOT_FOUND, 'فاکتور یافت نشد'))


# endregion S

# region Update Invoice Status
class UpdateInvoiceApiView(APIView):
    @extend_schema(
        request=ChangeInvoiceStatusSerializer,
        responses={200: ChangeInvoiceStatusSerializer},
    )
    def put(self, request: Request, invoice_id: int):
        permission_classes = [IsAuthenticated, CheckPermission]
        authentication_classes = JWTAuthentication

        invoice = get_invoice(invoice_id)
        if invoice is not None:
            serializer = ChangeInvoiceStatusSerializer(invoice, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    utilities.response_formatter(None, status.HTTP_404_NOT_FOUND, 'وضعیت سفارش با موفقیت تغییر کرد'))
        else:
            return Response(utilities.response_formatter(None, status.HTTP_404_NOT_FOUND, 'فاکتور یافت نشد'))


# endregion

# region Create Invoice

def get_product(product_id):
    try:
        product = Product.objects.get(id=product_id)
        return product
    except Product.DoesNotExist:
        return None


class CreateInvoiceApiView(APIView):
    @extend_schema(
        request=AddInvoiceSerializer,
        responses={200: AddInvoiceSerializer},
    )
    def post(self, request: Request):

        permission_classes = [IsAuthenticated, CheckPermission]
        authentication_classes = JWTAuthentication

        invoice_ser = AddInvoiceSerializer(data=request.data)
        user = CustomerUser.objects.get(id=request.user.id)

        if invoice_ser.is_valid():
            try:
                invoice = Invoice.objects.get(user=user, is_pay=False, is_returned=False)
            except:
                invoice = None

            if invoice is None:
                new_cart = Invoice.objects.create(
                    user=user,
                    tax_amount=0,
                    payable_amount=0,
                )
                InvoiceItem.objects.create(
                    invoice=new_cart,
                    product=get_product(invoice_ser.validated_data['product_id']),
                    count=invoice_ser.validated_data['qty']
                )
                detail = utilities.total_amount(new_cart.invoice_items.all())
                new_cart.payable_amount = detail.get('final_price')
                new_cart.save()
                return Response(utilities.response_formatter({
                    'invoice': InvoiceSerializer(instance=new_cart, many=False).data,
                    'invoice_detail': detail
                }, status.HTTP_200_OK, 'سبد خرید با موفقیت ایجاد شد'))
            else:
                new_item = InvoiceItem.objects.filter(product_id=invoice_ser.validated_data['product_id'],
                                                      invoice=invoice).first()
                if new_item is None:
                    InvoiceItem.objects.create(
                        invoice=invoice,
                        product=get_product(invoice_ser.validated_data['product_id']),
                        count=invoice_ser.validated_data['qty']
                    )

                else:
                    new_item.count += int(invoice_ser.validated_data['qty'])
                    new_item.save()

                detail = utilities.total_amount(invoice.invoice_items.all(), invoice.mixed_item.all())

                invoice.payable_amount = detail.get('final_price')
                invoice.save()

                return Response(utilities.response_formatter({
                    'invoice': InvoiceSerializer(instance=invoice, many=False).data,
                    'invoice_detail': detail
                }, status.HTTP_200_OK, 'سبد خرید با موفقیت بروز شد'))
        else:
            return Response(utilities.response_formatter(None, status.HTTP_400_BAD_REQUEST, 'خطای غیر منتظره'))


# endregion

# region Update Invoice Information

class UpdateInvoiceInformationApiView(APIView):
    @extend_schema(
        request=UpdateInvoiceInformationSerializer,
        responses={200: UpdateInvoiceInformationSerializer},
    )
    def post(self, request):
        permission_classes = [permissions.IsAuthenticated]

        serialize = UpdateInvoiceInformationSerializer(data=request.data)
        if serialize.is_valid():
            try:
                invoice = Invoice.objects.get(user=request.user, is_pay=False, is_returned=False)
            except:
                return Response(utilities.response_formatter(None, status.HTTP_404_NOT_FOUND, 'سبد خریدی وجود ندارد!'))

            invoice.receiver_address = serialize.validated_data['receiver_address']
            invoice.received_phone = serialize.validated_data['received_phone']
            invoice.received_full_name = serialize.validated_data['received_full_name']
            invoice.save()

            return Response(utilities.response_formatter(None, status.HTTP_200_OK, 'اطلاعات فاکتور با موفقیت ثبت شد!'))

        else:
            return Response(utilities.response_formatter(None, status.HTTP_400_BAD_REQUEST, 'مقادیر ارسالی صحیح نیست!'))


# endregion

# region Update Item of Invoice

class UpdateItemOfInvoiceApiView(APIView):
    @extend_schema(
        request=UpdateInvoiceItemSerializer,
        responses={200: UpdateInvoiceItemSerializer},
    )
    def put(self, request, item_id: int):
        permission_classes = [IsAuthenticated, CheckPermission]
        authentication_classes = JWTAuthentication

        try:
            invoice_item = InvoiceItem.objects.get(id=item_id)
        except:
            return Response(utilities.response_formatter(None, status.HTTP_404_NOT_FOUND, 'آیتم پیدا نشد!'))

        serializer = UpdateInvoiceItemSerializer(data=request.data)

        if serializer.is_valid():
            invoice_item.count = serializer.validated_data['qty']
            invoice_item.save()

            invoice = Invoice.objects.get(user=request.user, is_pay=False, is_returned=False)
            invoice.payable_amount = utilities.total_amount(invoice.invoice_items.all()).get('final_price')
            invoice.save()

            return Response(utilities.response_formatter(None, status.HTTP_200_OK, 'سبد خرید با موفقیت آپدیت شد!'))
        else:
            return Response(utilities.response_formatter(None, status.HTTP_400_BAD_REQUEST,
                                                         'مقادیر ارسالی به طور صحیح وارد نشده است!'))


# endregion

# region Remove Item To Invoice
class RemoveItemTOInvoiceApiView(APIView):
    def delete(self, request: Request, item_id: int):
        permission_classes = [IsAuthenticated, CheckPermission]
        authentication_classes = JWTAuthentication

        try:
            invoice_item = InvoiceItem.objects.get(id=item_id)
            invoice = Invoice.objects.get(user=request.user, is_pay=False, is_returned=False)
            invoice_item.delete()
            invoice.payable_amount = utilities.total_amount(invoice.invoice_items.all()).get('final_price')
            if len(invoice.invoice_items.all()) < 1 and len(invoice.mixed_item.all()) < 1:
                invoice.delete()
                return Response(utilities.response_formatter(None, status.HTTP_200_OK, 'سبد خرید شما حذف شد'))
            invoice.save()

            return Response(
                utilities.response_formatter(None, status.HTTP_200_OK, 'محصول از سبد خرید با موفقیت حذف شد'))
        except InvoiceItem.DoesNotExist:
            return Response(
                utilities.response_formatter(None, status.HTTP_404_NOT_FOUND, 'پارامتر ارسالی نا معتبر است'))


# endregion

# region Mix Item and Mixed


# region Create Mix Item

class CreateMixItemApiView(APIView):
    @extend_schema(
        request=AddItemMixSerializer,
        responses={200: MixItemSerializer},
    )
    def post(self, request: Request):
        permission_classes = [IsAuthenticated, CheckPermission]
        authentication_classes = JWTAuthentication

        serialize_data = AddItemMixSerializer(data=request.data)
        if serialize_data.is_valid():

            try:
                product = Product.objects.get(id=serialize_data.validated_data['product_id'])
            except Product.DoesNotExist:
                return Response(utilities.response_formatter(None, status.HTTP_404_NOT_FOUND, 'محصول پیدا نشد'))

            try:
                invoice = Invoice.objects.get(user=request.user, is_pay=False, is_returned=False)
            except Invoice.DoesNotExist:
                invoice = Invoice.objects.create(user=request.user, is_pay=False, is_returned=False, payable_amount=0)

            print('be inja mirese')

            total = int(product.product_after_discount) * int(serialize_data.validated_data['count'])

            new_mix_item = MixedItem.objects.create(product=product, count=serialize_data.validated_data['count'],
                                                    total_price=total)
            serializer_mix_item = MixItemSerializer(new_mix_item, many=False)

            return Response(utilities.response_formatter(serializer_mix_item.data, status.HTTP_200_OK,
                                                         'آیتم ترکیب با موفقیت ساخته شد'))
        else:
            return Response(
                utilities.response_formatter(None, status.HTTP_400_BAD_REQUEST, 'مقادیر به درستی ارسال نشده است'))


# endregion

# region Update Mix Item

class UpdateMixItemApiView(APIView):
    @extend_schema(
        request=UpdateItemMixSerializer,
        responses={200: MixItemSerializer},
    )
    def put(self, request):
        permission_classes = [IsAuthenticated, CheckPermission]
        authentication_classes = JWTAuthentication

        serializer = UpdateItemMixSerializer(data=request.data)
        if serializer.is_valid():

            try:
                mix_item = MixedItem.objects.get(id=serializer.validated_data['mix_item'])
            except MixedItem.DoesNotExist:
                return Response(utilities.response_formatter(None, status.HTTP_404_NOT_FOUND, 'آیتم ترکیب پیدا نشد!'))

            mix_item.count = serializer.validated_data['count']
            total = int(mix_item.product.product_after_discount) * int(serializer.validated_data['count'])
            mix_item.total_price = total
            mix_item.save()

            serialize_data = MixItemSerializer(mix_item, many=False)

            return Response(
                utilities.response_formatter(serialize_data.data, status.HTTP_200_OK, 'مقدار آیتم با موفقیت تغییر کرد'))


# endregion

# region Delete Mix Item

class DeleteMixItemApiView(APIView):
    @extend_schema(
        request=GetMixItemSerializer,
    )
    def delete(self, request, mix_item_id: int):
        permission_classes = [IsAuthenticated, CheckPermission]
        authentication_classes = JWTAuthentication

        try:
            mix_item = MixedItem.objects.get(id=mix_item_id)
            mix_item.delete()

            invoice = Invoice.objects.get(user=request.user, is_pay=False, is_returned=False)
            if len(invoice.invoice_items.all()) < 1 and len(invoice.mixed_item.all()) < 1:
                invoice.delete()

            return Response(utilities.response_formatter(None, status.HTTP_200_OK, 'آیتم ترکیب با موفقیت حذف شد!'))

        except MixedItem.DoesNotExist:
            return Response(utilities.response_formatter(None, status.HTTP_404_NOT_FOUND, 'آیتم ترکیب پیدا نشد!'))


# endregion

# region Create Mixed
class CreateMixedApiView(APIView):
    @extend_schema(
        request=AddMixedSerializer,
        responses={200: MixedSerializer},
    )
    def post(self, request: Request):
        permission_classes = [IsAuthenticated, CheckPermission]
        authentication_classes = JWTAuthentication

        serialize = AddMixedSerializer(data=request.data)
        if serialize.is_valid():
            try:
                invoice = Invoice.objects.get(user=request.user, is_pay=False, is_returned=False)
            except Invoice.DoesNotExist:
                invoice = Invoice.objects.create(user=request.user, is_pay=False, is_returned=False,
                                                 payable_amount=0)

            new_mixed = Mixed.objects.create(invoice=invoice, total_price=0)
            total = 0
            for item in serialize.validated_data['mix_items']:
                total += int(item.total_price)
                item.mix = new_mixed
                item.save()

            new_mixed.total_price = total
            new_mixed.save()

            serialize_data = MixedSerializer(new_mixed, many=False).data

            detail = utilities.total_amount(invoice.invoice_items.all(), invoice.mixed_item.all())
            print(detail)
            invoice.payable_amount = detail.get('final_price')
            invoice.save()

            return Response(
                utilities.response_formatter(serialize_data, status.HTTP_200_OK, 'ترکیب با موفقیت ساخته شد'))
        else:
            return Response(
                utilities.response_formatter(None, status.HTTP_400_BAD_REQUEST,
                                             'تعداد آیتم ها برای افزودن باید بیشتر از یکی باشد!'))


# endregion

# region Delete Mixed

class DeleteMixedApiView(APIView):

    @extend_schema(
        request=GetMixedSerializer,
    )
    def delete(self, request, mixed_item_id: int):
        permission_classes = [IsAuthenticated, CheckPermission]
        authentication_classes = JWTAuthentication

        try:
            mixed = Mixed.objects.get(id=mixed_item_id)
            for item in mixed.mix_items.all():
                item.delete()
            mixed.delete()

            return Response(utilities.response_formatter(None, status.HTTP_200_OK, 'ترکیب با موفقیت حذف شد'))

        except Mixed.DoesNotExist:
            return Response(utilities.response_formatter(None, status.HTTP_404_NOT_FOUND, 'ترکیب پیدا نشد!'))


# endregion


# endregion

# region Factor list user

class UserFactorListApiView(APIView):
    def get(self, request):
        permission_classes = [IsAuthenticated, CheckPermission]
        authentication_classes = JWTAuthentication

        factors = Invoice.objects.filter(user=request.user)
        serializer = InvoiceSerializer(factors, many=True)

        return Response(utilities.response_formatter(serializer.data, status.HTTP_200_OK, 'لیست فاکتور های پرداختی کاربر'))


# endregion
