from django.urls import path
from apps.main import views

app_name = 'main'
urlpatterns = [
    path('', views.SiteSettingApiView.as_view(), name='get_setting'),
    path('home/', views.HomeApiView.as_view(), name='home'),
    path('site_rules/', views.SiteRulesApiView.as_view(), name='get_site_rules'),
    path('social_media/', views.SocialMediaApiView.as_view(), name='get_social_media'),
    path('repetitive_questions/', views.RepetitiveQuestionsApiView.as_view(), name='repetitive_questions'),
]
