from django.urls import path
from apps.comment import views

app_name = 'comment'
urlpatterns = [
    path('', views.SubmitCommentApiView.as_view(), name='submit_commit'),
]
