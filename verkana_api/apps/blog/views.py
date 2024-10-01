# region Import Lib
from rest_framework.request import Request
from rest_framework.views import APIView

from .models import BlogCategory, Blog, BlogTag
from rest_framework.response import Response
from rest_framework import status
from apps import utilities

from drf_spectacular.utils import extend_schema

from .serializer import BlogSerializer, BlogCategorySerializer, BlogTagSerializer
# endregion


# region Blog
class BlogApiView(APIView):
    @extend_schema(
        request=BlogSerializer,
        responses={200: BlogSerializer},
    )
    def get(self, request: Request):
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(utilities.response_formatter(serializer.data, status.HTTP_200_OK, 'لیست مقاله ها'))


class BlogDetailApiView(APIView):
    @extend_schema(
        request=BlogSerializer,
        responses={200: BlogSerializer},
    )
    def get(self, request: Request, blog_id: int):
        try:
            blog = Blog.objects.get(id=blog_id)
            serializer = BlogSerializer(blog, many=False)
            return Response(utilities.response_formatter(serializer.data, status.HTTP_200_OK, 'جزئیات مقاله '))
        except Blog.DoesNotExist:
            return Response(utilities.response_formatter(None, status.HTTP_404_NOT_FOUND, 'مقاله یافت نشد'))


# endregion


# region Blog Category
class BlogCategoryApiView(APIView):
    @extend_schema(
        request=BlogCategorySerializer,
        responses={200: BlogCategorySerializer},
    )
    def get(self, request: Request):
        categories = BlogCategory.objects.all()
        serializer = BlogCategorySerializer(categories, many=True)
        return Response(utilities.response_formatter(serializer.data, status.HTTP_200_OK, 'لیست دیته بندی مقاله'))


class BlogCategoryDetailApiView(APIView):
    @extend_schema(
        request=BlogCategorySerializer,
        responses={200: BlogCategorySerializer},
    )
    def get(self, request: Request, blog_category_id: int):
        try:
            category = BlogCategory.objects.get(id=blog_category_id)
            serializer = BlogCategorySerializer(category, many=False)
            return Response(utilities.response_formatter(serializer.data, status.HTTP_200_OK, 'جزئیات دسته بندی مقاله'))
        except BlogCategory.DoesNotExist:
            return Response(utilities.response_formatter(None, status.HTTP_404_NOT_FOUND, 'دسته بندی یافت نشد'))


# endregion


# region Blog Tags
class BlogTagApiView(APIView):
    @extend_schema(
        request=BlogTagSerializer,
        responses={200: BlogTagSerializer},
    )
    def get(self, request: Request):
        tags = BlogTag.objects.all()
        serializer = BlogTagSerializer(tags, many=True)
        return Response(utilities.response_formatter(serializer.data, status.HTTP_200_OK, 'لیست تگهای مقاله'))


class BlogTagDetailApiView(APIView):
    @extend_schema(
        request=BlogTagSerializer,
        responses={200: BlogTagSerializer},
    )
    def get(self, request: Request, blog_tag_id: int):
        try:
            tag = BlogTag.objects.get(id=blog_tag_id)
            serializer = BlogTagSerializer(tag, many=False)
            return Response(utilities.response_formatter(serializer.data, status.HTTP_200_OK, 'جزئیات تک مقاله'))
        except BlogTag.DoesNotExist:
            return Response(utilities.response_formatter(None, status.HTTP_404_NOT_FOUND, 'تگ یافت نشد'))
# endregion
