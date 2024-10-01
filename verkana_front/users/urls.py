from django.urls import path
from . import views


app_name = 'user'

urlpatterns = [
    path('login/', views.LgoinView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('activate_account/', views.ActivateAccountView.as_view(), name='activate_account'),
    path('forget_password/', views.RecoveryPasswordView.as_view(), name='forget_password'),

    # region profile
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('orders/', views.UserOrders.as_view(), name='orders'),
    path('orders/<factor_id>/', views.UserOrderDetail.as_view(), name='orders_detail'),
    path('change_password/', views.ChangePasswordView.as_view(), name='change_password'),
    # endregion
]
