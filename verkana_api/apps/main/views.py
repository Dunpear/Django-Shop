from rest_framework.request import Request
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import status
from apps import utilities

from drf_spectacular.utils import extend_schema

from apps.main.models import SiteSettings, SiteRules, SocialMedia, RepetitiveQuestions, Advantages
from apps.product.models import *
from apps.blog.models import *
from apps.banner.models import *
from apps.slider.models import *
from apps.account.models import *

from apps.product.serializer import *
from apps.blog.serializer import *
from apps.banner.serializer import *
from apps.slider.serializer import *
from apps.account.serializer import *

from .serializer import (SocialMediaSerializer, SiteRulesSerializer, SiteSettingsSerializer,
                         RepetitiveQuestionsSerializer, AdvantagesSerializer)


class SiteSettingApiView(APIView):
    @extend_schema(
        request=SiteSettingsSerializer,
        responses={200: SiteSettingsSerializer},
    )
    def get(self, request: Request):
        site_settings = SiteSettings.objects.all()
        serializer = SiteSettingsSerializer(site_settings, many=True)
        return Response(utilities.response_formatter(serializer.data, status.HTTP_200_OK, 'لیست تنظمات سایت'))


class HomeApiView(APIView):
    def get(self, request):
        site_settings = SiteSettings.objects.all()
        site_settings_serializer = SiteSettingsSerializer(site_settings, many=True).data

        social_media = SocialMedia.objects.all()
        social_media_serializer = SocialMediaSerializer(social_media, many=True).data

        blogs = Blog.objects.all()
        blogs_serializer = BlogSerializer(blogs, many=True).data

        banner = Banner.objects.all()
        banner_serializer = BannerSerializer(banner, many=True).data

        if request.user.is_authenticated:
            user_serializer = CustomerUserSerializer(request.user, many=False).data
        else:
            user_serializer = None

        brands = Brand.objects.all()
        brands_serializer = BrandSerializer(brands, many=True).data

        product_groups = ProductGroup.objects.all()
        product_groups_serializer = ProductGroupSerializer(product_groups, many=True).data

        products = Product.objects.all()
        products_serializer = ProductSerializer(products, many=True).data

        sliders = Slider.objects.all()
        slider_serialize = SliderSerializer(sliders, many=True).data

        advantages = Advantages.objects.all()
        advantages_serializer = AdvantagesSerializer(advantages, many=True).data

        features = Feature.objects.all()
        features_serializer = FeatureSerializer(features, many=True).data

        result = {
            'site_settings': site_settings_serializer,
            'advantages': advantages_serializer,
            'social_media': social_media_serializer,
            'blogs': blogs_serializer,
            'banners': banner_serializer,
            'brands': brands_serializer,
            'sliders': slider_serialize,
            'product_groups': product_groups_serializer,
            'products': products_serializer,
            'user': user_serializer,
            'features': features_serializer
        }

        return Response(result, status=status.HTTP_200_OK)


class SiteRulesApiView(APIView):
    @extend_schema(
        request=SiteRulesSerializer,
        responses={200: SiteRulesSerializer},
    )
    def get(self, request: Request):
        site_rules = SiteRules.objects.all()
        serializer = SiteRulesSerializer(site_rules, many=True)
        return Response(utilities.response_formatter(serializer.data, status.HTTP_200_OK, 'لیست سیاست های سایت'))


class SocialMediaApiView(APIView):
    @extend_schema(
        request=SocialMediaSerializer,
        responses={200: SocialMediaSerializer},
    )
    def get(self, request: Request):
        social_media = SocialMedia.objects.all()
        serializer = SocialMediaSerializer(social_media, many=True)
        return Response(utilities.response_formatter(serializer.data, status.HTTP_200_OK, 'لیست شبکه های اجتماعی'))


class RepetitiveQuestionsApiView(APIView):
    def get(self, request: Request):
        repetitive_questions = RepetitiveQuestions.objects.all()
        serializer = RepetitiveQuestionsSerializer(repetitive_questions, many=True)
        return Response(utilities.response_formatter(serializer.data, status.HTTP_200_OK, 'لیست سوالات متداول'))


