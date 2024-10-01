from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import *
from drf_spectacular.utils import extend_schema

from .models import Slider, SliderItem
from .serializer import SliderSerializer, SliderItemSerializer
from apps import utilities


# region Slider
class ManageSliderApiView(APIView):
    @extend_schema(
        request=SliderSerializer,
        responses={200: SliderSerializer},
    )
    def get(self, request: Request):
        sliders = Slider.objects.all()
        slider_serialize = SliderSerializer(sliders, many=True)
        return Response(utilities.response_formatter(slider_serialize.data, status.HTTP_200_OK, 'لیست اسلایدر ها'))

# endregion
