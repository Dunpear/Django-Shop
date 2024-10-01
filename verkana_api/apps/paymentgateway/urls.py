from django.urls import path
from . import views

app_name = 'paymentgateway'
urlpatterns = [
    path('', views.RegistrationPayment.as_view(), name='index'),
    path('request_money/', views.MoneyRequestApiView.as_view(), name='money_request'),
    path('detail_transaction/<int:transaction_id>', views.DetailTransactionApiView.as_view(), name='detail_transaction')
]
