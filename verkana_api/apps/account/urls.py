from django.urls import path

from apps.account import views

app_name = 'account'
urlpatterns = [
    path('register/', views.CustomerUserManager.as_view(), name='customer'),
    path('manage/', views.CustomerUserDetailViewSet.as_view(), name='customer_manager'),
    path('active/', views.CustomerUserActiveAccountApiView.as_view(), name='active_account'),
    path('recovery/', views.RecoveryCustomerUserApiView.as_view(), name='recovery_account'),
    path('check_auth/', views.CheckAuthToken.as_view(), name='check_auth'),
    path('change_password/', views.ChangePasswordApiView.as_view(), name='change_password')
]
