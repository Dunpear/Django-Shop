from django.urls import path
from . import views

app_name = 'invoice'
urlpatterns = [
    path('get_current/', views.GetCurrentInvoiceApiView.as_view(), name='get_current_invoice'),
    path('get_invoice_list/', views.UserFactorListApiView.as_view(), name='get_invoice_list'),
    path('get_invoice/<int:invoice_id>', views.GetInvoiceApiView.as_view(), name='get_invoice'),
    path('change_invoice_status/<int:invoice_id>', views.UpdateInvoiceApiView.as_view(), name='change_invoice_status'),
    path('change_invoice_information/', views.UpdateInvoiceInformationApiView.as_view(), name='change_invoice_information'),
    path('create/', views.CreateInvoiceApiView.as_view(), name='create'),
    path('update/<int:item_id>', views.UpdateItemOfInvoiceApiView.as_view(), name='update'),
    path('remove/<int:item_id>', views.RemoveItemTOInvoiceApiView.as_view(), name='delete'),
    path('add_mix_item/', views.CreateMixItemApiView.as_view(), name='add_mix_item'),
    path('update_mix_item/', views.UpdateMixItemApiView.as_view(), name='update_mix_item'),
    path('add_mixed/', views.CreateMixedApiView.as_view(), name='add_mixed'),
    path('remove_mixed/<int:mixed_item_id>', views.DeleteMixedApiView.as_view(), name='remove_mixed'),
    path('remove_mix_item/<int:mix_item_id>', views.DeleteMixItemApiView.as_view(), name='remove_mix_item')
]
