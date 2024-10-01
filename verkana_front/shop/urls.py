from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [

    path('', views.Main.as_view(), name='main'),
    path('search/', views.Search.as_view(), name='search'),
    path('shop/', views.Shop.as_view(), name='shop'),

    # region details

    path('product_detail/<product_slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('category_detail/<int:category_id>/', views.CategoryDetailView.as_view(), name='category_detail'),

    # endregion

    # region others

    path('about_us/', views.AboutUsView.as_view(), name='about_us'),
    path('questions/', views.QuestionsView.as_view(), name='questions'),
    path('contact_us/', views.ContactUs.as_view(), name='contact_us'),

    # endregion


    # region comment
    path('comment/', views.SubmitCommentView.as_view(), name='comment'),
    # endregion


]