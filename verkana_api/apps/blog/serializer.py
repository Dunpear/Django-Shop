from rest_framework import serializers
from .models import Blog, BlogCategory, BlogTag


class BlogTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogTag
        fields = '__all__'


class BlogCategoryForOneBlogSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogCategory
        fields = '__all__'


class BlogSerializer(serializers.ModelSerializer):
    tags = BlogTagSerializer(many=True, read_only=True)
    category = BlogCategoryForOneBlogSerializer(many=False, read_only=True)

    class Meta:
        model = Blog
        fields = ['id', 'title', 'description', 'picture', 'picture_alt', 'picture_title', 'width', 'height',
                  'meta_keyword', 'meta_description', 'register_date', 'tags', 'category', 'is_active']


class BlogCategorySerializer(serializers.ModelSerializer):
    blogs = BlogSerializer(many=True, read_only=True)

    class Meta:
        model = BlogCategory
        fields = ['id', 'title', 'slug', 'register_date', 'picture', 'picture_alt', 'picture_title', 'width', 'height',
                  'blogs']

