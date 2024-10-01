from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
                  # region Main Url
                  path('', include('apps.main.urls', namespace='main')),
                  # endregion

                  # region admin-CkEditor
                  path('admin/', admin.site.urls),
                  path('ckeditor', include('ckeditor_uploader.urls')),
                  # endregion

                  # region Accounting Urls
                  path('account/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                  path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
                  path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
                  path('account/', include('apps.account.urls', namespace='account')),
                  # endregion

                  # region Slider-Banner Urls
                  path('slider/', include('apps.slider.urls', namespace='slider')),
                  path('banner/', include('apps.banner.urls', namespace='banner')),

                  # endregion

                  # region blogs
                  path('blog/', include('apps.blog.urls', namespace='blog')),
                  # endregion

                  # region Products Url
                  path('product/', include('apps.product.urls', namespace='products')),
                  # endregion

                  # region comment
                  path('comment/', include('apps.comment.urls', namespace='comment')),
                  # endregion

                  # region Invoice
                  path('invoices/', include('apps.invoice.urls', namespace='invoice')),
                  # endregion

                  # region Payment Gateway
                  path('payment/', include('apps.paymentgateway.urls', namespace='paymentgateway')),
                  # endregion

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'پنل مدیریت فروشگاه'
