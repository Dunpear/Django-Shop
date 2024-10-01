from . import views
from django.urls import path


app_name = 'blog'

urlpatterns = [
    path('', views.BlogListView.as_view(), name='blog_list'),
    path('detail/<int:blog_id>', views.BlogDetailView.as_view(), name='blog_detail'),
    path('category_detail/<int:category_id>', views.CategoryDetailView.as_view())
]