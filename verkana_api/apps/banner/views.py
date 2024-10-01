from django.shortcuts import render
from rest_framework.views import APIView

from .models import Banner
from .serializer import BannerSerializer
from rest_framework.response import Response
from rest_framework import status
from apps import utilities

from drf_spectacular.utils import extend_schema


class BannerApiView(APIView):
    @extend_schema(
        request=BannerSerializer,
        responses={200: BannerSerializer},
    )
    def get(self, request):
        banner = Banner.objects.all()
        serializer = BannerSerializer(banner, many=True)

        return Response(utilities.response_formatter(serializer.data, status.HTTP_200_OK, 'لیست بنر ها'))
