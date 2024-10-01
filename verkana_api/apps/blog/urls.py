from django.urls import path
from apps.blog import views

app_name = 'blog'
urlpatterns = [
    path('', views.BlogApiView.as_view(), name='get_blogs'),
    path('<int:blog_id>', views.BlogDetailApiView.as_view(), name='get_blog_detail'),

    path('category/', views.BlogCategoryApiView.as_view(), name='get_blogs_category'),
    path('category/<int:blog_category_id>', views.BlogCategoryDetailApiView.as_view(), name='get_blogs_category_detail'),

    path('tag/', views.BlogTagApiView.as_view(), name='get_blogs_tag'),
    path('tag/<int:blog_tag_id>', views.BlogTagDetailApiView.as_view(), name='get_blogs_tag_detail'),
]
