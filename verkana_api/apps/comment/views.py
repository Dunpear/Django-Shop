from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from apps import utilities
from .serializer import SubmitCommentSerializer, ProductCommentSerializer
from drf_spectacular.utils import extend_schema
from .models import ProductComment




class SubmitCommentApiView(APIView):
    @extend_schema(
        request=SubmitCommentSerializer,
        responses={200: ProductCommentSerializer},
    )
    def post(self, request: Request):
        serilizer = SubmitCommentSerializer(data=request.data)
        if serilizer.is_valid():

            new_comment = ProductComment.objects.create(**serilizer.validated_data, user=request.user)

            return Response(utilities.response_formatter(None, status.HTTP_200_OK, 'نظر شما ثبت گرید. باتشکر'))
        else:
            return Response(utilities.response_formatter(None, status.HTTP_400_BAD_REQUEST, 'مقدار فیلد ها صحیح نیست'))
