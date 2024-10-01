from django.urls import path

from apps.slider import views

app_name = 'slider'
urlpatterns = [
    path('', views.ManageSliderApiView.as_view(), name='slider')
]
