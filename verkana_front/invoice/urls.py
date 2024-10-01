from django.urls import path
from . import views

app_name = 'invoice'

urlpatterns = [
    path('', views.DetailCartView.as_view(), name='detail_cart'),
    path('delete_item/', views.DeleteItemView.as_view(), name='delete_item'),
    path('add_productitem/', views.AddProductItem.as_view(), name='add_productitem'),
    path('update_productitem/', views.UpdateProductItem.as_view(), name='update_productitem'),
    path('check_out/', views.CheckOutView.as_view(), name='check_out'),
    path('payment/', views.send_request, name='payment'),
    path('verify_payment/', views.verify, name='verify_payment')
]
