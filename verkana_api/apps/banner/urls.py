from django.urls import path
from .views import BannerApiView
from apps.banner import views

app_name = 'banner'
urlpatterns = [
    path('', BannerApiView.as_view(), name='banners')
]
