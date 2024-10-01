from django.db.models import Q
from django.shortcuts import render

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, extend_schema_field
from drf_spectacular.types import OpenApiTypes
from apps import utilities
from .serializer import (BrandSerializer, ProductGroupSerializer, FeatureSerializer, ProductGallerySerializer,
                         ProductSerializer, ProductBodyParamSearchSerializer, ProductBodyParamFilterSerializer)
from .models import (Product, ProductGroup, ProductGallery, Brand, ProductFeature, ProductTag, Feature)

from urllib.parse import unquote


# region Brands
class BrandApiView(APIView):
    @extend_schema(
        request=BrandSerializer,
        responses={200: BrandSerializer},
    )
    def get(self, request: Request):
        brands = Brand.objects.all()
        serializer = BrandSerializer(brands, many=True)
        return Response(utilities.response_formatter(serializer.data, status.HTTP_200_OK, 'لیست برند ها'))


# endregion

# region Product Group
class ProductGroupApiView(APIView):
    @extend_schema(
        request=ProductGroupSerializer,
        responses={200: ProductGroupSerializer},
    )
    def get(self, request: Request):
        product_groups = ProductGroup.objects.all()
        serializer = ProductGroupSerializer(product_groups, many=True)
        return Response(utilities.response_formatter(serializer.data, status.HTTP_200_OK, 'لیست دسته بندی ها'))


# endregion

# region ProductGroup Feature
class ProductGroupFeatureApiView(APIView):
    @extend_schema(
        request=FeatureSerializer,
        responses={200: FeatureSerializer},
    )
    def get(self, request: Request):
        features = Feature.objects.all()
        serializer = FeatureSerializer(features, many=True)
        return Response(utilities.response_formatter(serializer.data, status.HTTP_200_OK, 'لیست ویژگی ها'))


# endregion

# region Product Gallery
class ProductGalleryApiView(APIView):
    @extend_schema(
        request=ProductGallerySerializer,
        responses={200: ProductGallerySerializer},
    )
    def get(self, request: Request):
        gallery = ProductGallery.objects.all()
        serializer = ProductGallerySerializer(gallery, many=True)
        return Response(utilities.response_formatter(serializer.data, status.HTTP_200_OK, 'لیست گالری محصولات'))


# endregion

# region Product
class ProductApiView(APIView):
    @extend_schema(
        request=ProductSerializer,
        responses={200: ProductSerializer},
    )
    def get(self, request: Request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response({'products': serializer.data})


# endregion

# region Product Mixin

class GetProductMixinApiView(APIView):
    def get(self, request: Request):

        products = Product.objects.filter(is_mixin=True)
        serializer = ProductSerializer(products, many=True)

        return Response(utilities.response_formatter(serializer.data, status.HTTP_200_OK, 'لیست محصولات قابل ترکیب'))

# endregion

# region Product of Category

class ProductOfCategoryApiView(APIView):
    @extend_schema(
        request=ProductSerializer,
        responses={200: ProductSerializer},
    )
    def get(self, request, category_id):

        # چک میکنیم دسته بندی وجود داشته باشه
        try:
            category = ProductGroup.objects.get(id=category_id)
        except ProductGroup.DoesNotExist:
            return Response(utilities.response_formatter(None, status.HTTP_404_NOT_FOUND, 'دسته بندی پیدا نشد!'))

        # محصولاتی که درون این دسته بندی هستن رو به دست میاریم
        products = Product.objects.filter(product_group=category)
        serializer = ProductSerializer(products, many=True)

        # سریالایز میکنیم و نتیجه رو برمیگردونیم
        return Response(
            utilities.response_formatter(serializer.data, status.HTTP_200_OK, f' لیست محصولات دسته بندی {category} '))


# endregion

# region Product of Brand

class ProductOfBrandApiView(APIView):
    @extend_schema(
        request=ProductSerializer,
        responses={200: ProductSerializer},
    )
    def get(self, request, brand_id):

        # چک میکنیم برند وجود داشته باشه
        try:
            brand = Brand.objects.get(id=brand_id)
        except ProductGroup.DoesNotExist:
            return Response(utilities.response_formatter(None, status.HTTP_404_NOT_FOUND, 'برند پیدا نشد!'))

        # محصولاتی که این برند داره رو به دست میاریم!
        products = Product.objects.filter(brand=brand)
        serializer = ProductSerializer(products, many=True)

        # سریالایز میکنیم و نتیجه رو برمیگردونیم
        return Response(
            utilities.response_formatter(serializer.data, status.HTTP_200_OK, f' لیست محصولات برند {brand} '))


# endregion

# region Get Product by Slug
class GetProductBySlugApiView(APIView):
    @extend_schema(
        request=ProductSerializer,
        responses={200: ProductSerializer},
    )
    def get(self, request, slug):
        # چک میکنیم محصولی با این اسلاگ داشته باشیم
        try:
            product = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            return Response(utilities.response_formatter(None, status.HTTP_200_OK, 'محصول پیدا نشد!'))

        product.product_view_count += 1
        product.save()

        # به تعداد بازدید محصول یکی اضافه میکنیم!

        # محصول رو سریالایز و نتیجه رو برمیگردونیم
        serializer = ProductSerializer(product, many=False)
        return Response(utilities.response_formatter(serializer.data, status.HTTP_200_OK, f' اطلاعات محصول {product} '))


# endregion

# region Product Order
class ProductSortedApiView(APIView):
    @extend_schema(
        request=ProductSerializer,
        responses={200: ProductSerializer},
        parameters=[
            OpenApiParameter(name='order',
                             description='مرتب سازی بر اساس : (price_g,price_l,view,new,old,discount,)',
                             required=False, type=str),
        ],
    )
    def get(self, request):
        order = request.GET.get('order')
        products = Product.objects.all()
        order_name = ''

        if order == None:
            order_name = 'فیلتری پیدا نشد!'
        elif order == 'price_g':  # بیشترین قیمت
            products = products.order_by('-sell_price')
            order_name = 'بیشترین قیمت'
        elif order == 'price_l':  # کمترین قیمت
            products = products.order_by('sell_price')
            order_name = 'کمترین قیمت'
        elif order == 'new':  # جدید ترین ها بر اساس تاریخ ثبت
            products = products.order_by('-register_date')
            order_name = 'جدی ترین ها'
        elif order == 'old':  # قدیمی ترین ها بر اساس تاریخ ثبت
            products = products.order_by('register_date')
            order_name = 'قدیمی ترین ها'
        elif order == 'discount':  # بر اساس تخفیف
            products = products.order_by('-product_discount')
            order_name = 'بیشترین تخفیف'
        elif order == 'view':  # بر اساس بازدید محصولات
            products = products.order_by('-product_view_count')
            order_name = 'پر بازدید ترین ها'
        else:
            order_name = 'فیلتری پیدا نشد!'
        # elif order == 'rate':  need to add comments !
        #     pass

        serialize = ProductSerializer(products, many=True)

        return Response(
            utilities.response_formatter(serialize.data, status.HTTP_200_OK, f'{order_name}'))


# endregion

# region Product Filter
class ProductFilterApiView(APIView):
    @extend_schema(
        request=ProductBodyParamFilterSerializer,
        responses={200: ProductSerializer},
    )
    def post(self, request: Request, *args, **kwargs):
        products = Product.objects.all()
        price_lt = request.data.get('price_lt')
        price_gt = request.data.get('price_gt')
        brand_id = request.data.get('brand')
        category_id = request.data.get('category')
        if price_lt:
            products = products.filter(sell_price__gt=price_lt)
        if price_gt:
            products = products.filter(sell_price__lt=price_gt)
        if category_id:
            products = products.filter(product_group__in=[category_id])
        if brand_id:
            products = products.filter(brand__in=[brand_id])
        serializer = ProductSerializer(products, many=True)
        return Response(utilities.response_formatter(serializer.data, status.HTTP_200_OK, 'نتیجه فیلتر محصولات'))


# endregion

# region ProductSearch

class ProductSearchApiView(APIView):
    @extend_schema(
        request=ProductBodyParamSearchSerializer,
        responses={200: ProductSerializer},
    )
    def post(self, request: Request):
        try:
            product_name = request.data['product_name']
            category_id = request.data['category_id']

            if category_id == None or category_id == 'all':
                products = Product.objects.filter(
                    Q(product_name__contains=product_name) | Q(short_description__contains=product_name))
            else:

                try:
                    group = ProductGroup.objects.get(id=category_id)
                    products = Product.objects.filter(
                        Q(product_name__contains=product_name) | Q(short_description__contains=product_name), product_group=group)
                except:
                    products = Product.objects.filter(
                        Q(product_name__contains=product_name) | Q(short_description__contains=product_name))


            if products:
                serializer = ProductSerializer(products, many=True)
                return Response(utilities.response_formatter(serializer.data, status.HTTP_200_OK, 'نتیجه جستجو'))
            else:
                return Response(utilities.response_formatter(None, status.HTTP_404_NOT_FOUND, 'محصولی یافت نشد'))
        except:
            return Response(utilities.response_formatter(None, status.HTTP_400_BAD_REQUEST,
                                                         'فیلد نام را در بدنه درخواست پر نکردید'))




# endregion
