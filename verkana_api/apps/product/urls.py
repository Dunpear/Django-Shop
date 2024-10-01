from django.urls import path, re_path

from apps.product import views

app_name = 'products'
urlpatterns = [
    path('', views.ProductApiView.as_view(), name="get_products"),
    path('brand/', views.BrandApiView.as_view(), name="get_brand"),
    path('product_group/', views.ProductGroupApiView.as_view(), name="get_product_group"),
    path('features/', views.ProductGroupFeatureApiView.as_view(), name="get_features"),
    path('gallery/', views.ProductGalleryApiView.as_view(), name="get_galeries"),

    path('product_of_category/<int:category_id>', views.ProductOfCategoryApiView.as_view(), name='product_of_category'),
    path('product_of_brand/<int:brand_id>', views.ProductOfBrandApiView.as_view(), name='product_of_category'),
    # برای استفاده از مقادیر فارسی توی url باید از این ریجکس استفاده کنیم و همینطور از re path
    re_path(r'get_product/(?P<slug>[^/]+)/?$', views.GetProductBySlugApiView.as_view(), name="product_detail_by_slug"),
    path('product_orders/', views.ProductSortedApiView.as_view(), name="product_orders"),
    path('product_filter/', views.ProductFilterApiView.as_view(), name="product_filter"),
    path('product_search/', views.ProductSearchApiView.as_view(), name="product_search"),

    path('mixin/', views.GetProductMixinApiView.as_view(), name="mixin_get_list"),

]
