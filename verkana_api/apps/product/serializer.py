from rest_framework import serializers
from .models import (Brand, Product, ProductFeature, ProductTag, ProductGroup, ProductGallery, Feature)
from apps.comment.serializer import ProductCommentSerializer


# region Brand
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


# endregion

# region Group Feature
class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = '__all__'


# endregion

# region Product Group
class ProductGroupSerializer(serializers.ModelSerializer):
    category_features = FeatureSerializer(many=True, read_only=True)

    class Meta:
        model = ProductGroup
        fields = ['id', 'group_title', 'group_image', 'group_image_alt', 'group_image_title', 'width', 'height',
                  'css_class',
                  'css_style', 'description', 'meta_description', 'meta_keywords', 'is_active', 'register_date', 'slug',
                  'group_parent', 'category_features']


# endregion

# region Gallery
class ProductGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGallery
        fields = '__all__'


# endregion

# region Product Tags
class ProductTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTag
        fields = '__all__'


# endregion

# region Product Features
class ProductFeatureSerializer(serializers.ModelSerializer):
    group_features = FeatureSerializer(many=True, read_only=True)
    feature = FeatureSerializer(many=False, read_only=True)

    class Meta:
        model = ProductFeature
        fields = ['id', 'product', 'feature_value', 'feature', 'group_features', 'is_active']


# endregion

# region Product
class ProductInGroupsSerializer(serializers.Serializer):
    class Meta:
        model = ProductGroup
        fields = '__all__'


class ProductForInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id',
                  'product_name', 'cover_picture', 'group_image_alt', 'group_image_title', 'width', 'height',
                  'css_class',
                  'css_style', 'sell_price', 'product_discount', 'product_after_discount', 'slug', 'exist_count', ]


class ProductSerializer(serializers.ModelSerializer):
    product_features = ProductFeatureSerializer(many=True, read_only=True)
    brand = BrandSerializer(many=False, read_only=True)
    product_group = ProductGroupSerializer(many=True, read_only=True)
    tags = ProductTagSerializer(many=True, read_only=True)
    product_gallery = ProductGallerySerializer(many=True, read_only=True)
    product_comment = ProductCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id',
                  'product_name', 'short_description', 'full_description', 'cover_picture', 'group_image_alt',
                  'group_image_title', 'width', 'height', 'css_class', 'css_style', 'purchase_price', 'sell_price',
                  'product_discount', 'product_after_discount', 'slug', 'exist_count', 'product_view_count',
                  'product_sell_count', 'is_active', 'is_deleted', 'register_date', 'updated_date', 'user',
                  'product_features', 'brand', 'tags', 'product_group', 'product_gallery', 'product_comment']


class ProductBodyParamSearchSerializer(serializers.Serializer):
        product_name = serializers.CharField()
        category_id = serializers.CharField(default='all / category_id like: 1 or 2 or 3 ...')


class ProductBodyParamFilterSerializer(serializers.Serializer):
    price_lt = serializers.IntegerField()
    price_gt = serializers.IntegerField()
    brand_id = serializers.CharField()
    category_id = serializers.CharField()
# endregion
